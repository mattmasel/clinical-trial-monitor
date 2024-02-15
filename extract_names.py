import csv
import requests
from pathlib import Path

NASDAQ_LIST = Path('lists/nasdaq.csv')
COMPANY_EXTENSIONS = ['inc.', 'ltd.', 'corp.', 'co.', 'incorporated', 'limited', 'corporation', 'holding', 'group']

def extract_names(company_csv_list):
  search_expressions = []
  with open(company_csv_list, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csv_reader:
      company_name = row[1].split()
      for word in reversed(company_name):
        if word.lower() in COMPANY_EXTENSIONS:
          company_name.remove(word)
      search_expressions.append(' '.join(company_name))
  
  return search_expressions

def create_url_query(company_name):
  return f'https://classic.clinicaltrials.gov/api/query/study_fields?expr={company_name}\
  &fields=BriefTitle%2CBriefSummary%2CStartDate%2CCompletionDate&min_rnk=1&max_rnk=1000&fmt=json'

def get_trial_information(company_list):
  for company_name in company_list:
    request = requests.get(create_url_query(company_name))
    if request.status_code == 200:
      print(request.json())

if __name__ == '__main__':
  nasdaq_companies = extract_names(NASDAQ_LIST)
  get_trial_information(nasdaq_companies)