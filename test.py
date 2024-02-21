import yfinance as yf
from datetime import datetime, timedelta

def get_all_prices(ticker):
  company = yf.Ticker(ticker)
  # data = company.history(start=start_date, end=end_date)
  data = company.history(period="max")
  return data

def get_price_range(company_data, start_date, end_date):
  count = 1
  while len(company_data.loc[start_date:end_date]) != 3:
    start_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=count)).strftime('%Y-%m-%d')
    end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=count)).strftime('%Y-%m-%d')
    count += 1
  print(count)
  return company_data.loc[start_date:end_date]

if __name__ == '__main__':
  ixhl_data = get_all_prices('IXHL')
  print(ixhl_data)

  price_average = get_price_range(ixhl_data, '2024-01-13', '2024-01-15')
  print(price_average['Close'].values)

