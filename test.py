import yfinance as yf

def get_all_prices(ticker):
  company = yf.Ticker(ticker)
  # data = company.history(start=start_date, end=end_date)
  data = company.history(period="max")
  return data

def get_price_range(company_data, start_date, end_date):
  return company_data.loc[start_date:end_date]

if __name__ == '__main__':
  ixhl_data = get_all_prices('IXHL')
  print(ixhl_data)
  print(get_price_range(ixhl_data, '2024-02-14', '2024-02-16'))
  print(get_price_range(ixhl_data, '2024-01-20', '2024-01-23'))

