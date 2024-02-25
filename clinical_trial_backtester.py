import csv
import warnings
import requests
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path

NASDAQ_LIST           = Path('lists', 'nasdaq.csv')
TEST_LIST             = Path('lists', 'test_list.csv')
COMPANY_EXTENSIONS    = ['inc.', 'ltd.', 'corp.', 'co.', 'incorporated', 'limited', 'corporation', 'holding', 'holdings', 'group']
OUTPUT_CSV_FILE_PATH  = Path('results', 'output.csv')

# Clinical Trial API Fields
ID         = 'NCTId'
STATUS     = 'OverallStatus'
START_DATE = 'StudyFirstSubmitQCDate'
END_DATE   = 'CompletionDate'

warnings.filterwarnings("ignore", message="The 'unit' keyword in TimedeltaIndex construction is deprecated*")

def extract_names(company_csv_list):
  """
  Extracts the company names from a csv file of publicly listed companies.

  While extracting the company names it also trims the company type from the string. 
  For example it removes Inc. from the company name Test Company Inc.

  Parameters:
  company_csv_list (str): The path to the csv file cotaining company_csv_list.

  Returns:
  list of str: The cleaned company names.
  """
  search_expressions = []
  with open(company_csv_list, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(csv_reader)
    for row in csv_reader:
      company_name = row[1].split()
      ticker = row[2]
      for word in reversed(company_name):
        if word.lower() in COMPANY_EXTENSIONS:
          company_name.remove(word)
      expression = [' '.join(company_name), ticker]
      # search_expressions.append(' '.join(company_name))
      search_expressions.append(expression)
  
  return search_expressions

# Note: The new API will be taking effect as of mid-2024 and will need to be changed to the following format:
# https://clinicaltrials.gov/api/v2/studies?query.term=incannex
def create_url_query(company_name):
  return f'https://classic.clinicaltrials.gov/api/query/study_fields?expr={company_name}\
  &fields={ID}%2C{STATUS}%2C{START_DATE}%2C{END_DATE}&min_rnk=1&max_rnk=1000&fmt=json'

def get_trial_information(company_list):
  """
  Sends a query to clinicaltrials.gov using create_url_query() to generate the url for each unique company in the company list.

  Parameters:
  company_list (list of str): The company name to use ass the search expression in the get request.

  Returns:
  list: The companies that are soon (need to work out a cutoff) to start clinical trials.
  """
  all_company_data = []

  for company_name in company_list:
    request = requests.get(create_url_query(company_name[0]))
    if request.status_code == 200:
      # This is where we need to process the JSON data to extract the relevant information such as StartDate if >= todays date
      current_company_csv = process_json(request.json(), company_name[1])
      all_company_data.append(current_company_csv)

      for trial in current_company_csv:
        print(trial)
  
  return all_company_data

def process_json(json_data, ticker):
  """
  Processes the json response returned by the get_trial_information() request.
  
  Extracts the NCTId, OverallStatus, StudyFirstPostDate, StartDate, and CompletionDate for each rank.

  Parameters:
  json_data (dict): The json needed to be processed

  Returns:
  list: The relevant data necessary for further company analysis
  """
  csv_list = []

  study_fields_response = json_data['StudyFieldsResponse']
  field_list = study_fields_response.get('FieldList', [])
  study_fields = study_fields_response.get('StudyFields', [])
  expression = study_fields_response.get('Expression', '')

  extracted_data = []

  # Get historical stock prices for company
  company_daily_prices = get_prices(ticker)

  for trial in study_fields:
    extracted_study = {
      field: trial.get(field, [''])[0] if trial.get(field) else '' for field in field_list
    }
    extracted_study['CompanyName'] = expression
    extracted_study['Ticker'] = ticker
    extracted_data.append(extracted_study)
  
  return add_price_data(extracted_data, company_daily_prices, csv_list)
  # return extracted_data

def add_price_data(json_data, company_daily_prices, csv_list):
  """
  For each trial a company has on clinicaltrials.gov extract the trials before todays date.

  If date less than todays date, pass to price extractor to find prices and then calculate differences.

  Parameters:
  json_data (list of dicts): The trials for a company.

  Returns:
  List of dicts containing CompanyName, StudyFirstPostDate,StartDate,CompletionDate,StartPrice,EndPrice,PercentageDifference.
  Note: Rename from print json to parse json?
  """
  for trial in json_data:
    start_date = convert_date_format(trial[START_DATE])
    if start_date is not None and start_date <= datetime.today().strftime('%Y-%m-%d'):
      # WE SHOULD DOWNLOAD THE DATA ONCE PER COMPANY AND THEN USE THAT DATA TO FIND TRIAL PRICE INFORMATION.
      # THIS WILL REDUCE THE NUMBER OF yfinance REQUESTS BY A FACTOR OF AROUND 5
      buy_price, sell_price = get_price(company_daily_prices, start_date)
      # start_price, end_price = get_price(trial['Ticker'],trial['StartDate'])
      if buy_price or sell_price is not None:
        price_difference = ((sell_price - buy_price) / (buy_price + sell_price) / 2) * 100
        csv_list.append([
          trial['Ticker'], 
          trial[ID], 
          trial[START_DATE],
          trial[END_DATE],
          f"{buy_price:.2f}",
          f"{sell_price:.2f}",
          f"{price_difference:.2f}"
        ])

  return csv_list

def get_prices(ticker):
  ticker_data = yf.Ticker(ticker)
  # data = company.history(start=start_date, end=end_date)
  return ticker_data.history(period="max")

def get_price_range(company_data, start_date, end_date):
  """
  Iterates the start_date forward one day until it finds a three day range.

  If start_date is greater than 10 days past the trial start_date it will ignore that trial.

  Parameters:
  company_data (DataFrame): Contains all daily prices for a given ticker.
  start_date (str): The start date of the given clinical trial.
  end_date (str): The date 3 days after the given clinical trial.

  Returns:
  DataFrame containing the ticker prices for three days starting at the start_date.
  """
  count = 1
  while len(company_data.loc[start_date:end_date]) != 3:
    if count > 10:
      return None
    start_date, end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=count)).strftime('%Y-%m-%d'), \
    (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=count)).strftime('%Y-%m-%d')
    count += 1
  # print(count)
  return company_data.loc[start_date:end_date]

def get_price(company_daily_prices, start_date):
  """
  Note: The format for date is 2024-02-13
  """
  sell_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=3)).strftime('%Y-%m-%d')

  price_data = get_price_range(company_daily_prices, start_date, sell_date)

  #  Fix this tomorrow
  if price_data is None:
    return None, None
  
  buy_price = price_data['Close'].values[0]
  sell_price = price_data['Close'].values[2]
  return buy_price, sell_price

def convert_date_format(date) -> str:
  """
  Converts date from July 01, 2023 -> 2023-07-01
  """
  try:
    date_obj = datetime.strptime(date, '%B %d, %Y')
  except ValueError:
    try:
      date_obj = datetime.strptime(date, '%B %Y')
    except ValueError:
      return None
  
  formatted_date = date_obj.strftime('%Y-%m-%d')
  return formatted_date

def get_average_percent_change(company_csv_data) -> float:
  """
  Calculates the average percentage change for all trials

  Parameters:
  company_csv_data (list of lists): Contains all price differences in percent for each trial start date.

  Returns:
  The average percent change for all trials
  """
  sum_percent_change, count = 0, 0

  for company in company_csv_data:
    for trial in company:
      try:
        percent_change = float(trial[-1])
        sum_percent_change += percent_change
        count += 1
      except ValueError:
        print(f"Error converting value to float: {trial[-1]}")
  
  if count == 0:
    return 0

  return sum_percent_change / count

def save_to_csv(company_csv_data):
  with open(OUTPUT_CSV_FILE_PATH, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Ticker',ID,START_DATE,END_DATE,'BuyPrice','SellPrice','PercentDiff'])
    for company in company_csv_data:
      for row in company:
        writer.writerow(row)
    print(f"Data saved to {OUTPUT_CSV_FILE_PATH}")

if __name__ == '__main__':
  nasdaq_companies = extract_names(NASDAQ_LIST)
  company_csv_data = get_trial_information(nasdaq_companies)
  save_to_csv(company_csv_data)
  print(get_average_percent_change(company_csv_data))

  # TODO 1: Fix output_csv file format, currently it is keeping the "[]" and needs to be removed

