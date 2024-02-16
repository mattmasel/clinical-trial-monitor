import csv
import json
import requests
from pathlib import Path

TEST_LIST          = Path('lists/test_list.csv')
NASDAQ_LIST        = Path('lists/nasdaq.csv')
COMPANY_EXTENSIONS = ['inc.', 'ltd.', 'corp.', 'co.', 'incorporated', 'limited', 'corporation', 'holding', 'group']

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
      for word in reversed(company_name):
        if word.lower() in COMPANY_EXTENSIONS:
          company_name.remove(word)
      search_expressions.append(' '.join(company_name))
  
  return search_expressions

def create_url_query(company_name):
  return f'https://classic.clinicaltrials.gov/api/query/study_fields?expr={company_name}\
  &fields=NCTId%2COverallStatus%2CStudyFirstPostDate%2CStartDate%2CCompletionDate&min_rnk=1&max_rnk=1000&fmt=json'

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
    request = requests.get(create_url_query(company_name))
    if request.status_code == 200:
      # This is where we need to process the JSON data to extract the relevant information such as StartDate if >= todays date
      all_company_data.append(process_json(request.json()))
  
  return all_company_data

def process_json(json_data):
  """
  Processes the json response returned by the get_trial_information() request.
  
  Extracts the NCTId, OverallStatus, StudyFirstPostDate, StartDate, and CompletionDate for each rank.

  Parameters:
  json_data (dict): The json needed to be processed

  Returns:
  list: The relevant data necessary for further company analysis
  """
  study_fields_response = json_data['StudyFieldsResponse']
  field_list = study_fields_response.get('FieldList', [])
  study_fields = study_fields_response.get('StudyFields', [])
  expression = study_fields_response.get('Expression', '')

  extracted_data = []

  for trial in study_fields:
    extracted_study = {
      field: trial.get(field, [''])[0] if trial.get(field) else '' for field in field_list
    }
    extracted_study['CompanyName'] = expression
    extracted_data.append(extracted_study)
  print_json(extracted_data)
  return extracted_data

def print_json(json_data):
  for trial in json_data:
    print(
      f"{trial['CompanyName']:20} | {trial['NCTId']:11} | "
      f"Posted: {trial['StudyFirstPostDate']:17} | "
      f"StartDate: {trial['StartDate']:17} | "
      f"CompletionDate: {trial['CompletionDate']}"
    )

if __name__ == '__main__':
  nasdaq_companies = extract_names(NASDAQ_LIST)
  company_json_data = get_trial_information(nasdaq_companies)
  # print_json(company_json_data)