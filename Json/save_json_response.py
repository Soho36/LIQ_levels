import requests
import json
from config import api_key

# api_key = 'DEMO'

symbol = 'BTCUSD'
interval = '1min'

time_series_daily = False
time_series_intraday = True
output_size_full = True     # Query the most recent full 30 days of intraday data (or 100 bars by default)


def request_url_constructor():
    request_url_var = None

    if time_series_daily and output_size_full:
        request_url_var = (f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&'
                           f'outputsize=full&apikey={api_key}')

    elif time_series_daily and output_size_full is False:
        request_url_var = (f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&'
                           f'symbol={symbol}&apikey={api_key}')

    elif time_series_intraday and output_size_full:
        request_url_var = (f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&'
                           f'interval={interval}&outputsize=full&apikey={api_key}')

    elif time_series_intraday and output_size_full is False:
        request_url_var = (f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&'
                           f'interval={interval}&apikey={api_key}')

    else:
        print('Wrong input')

    return request_url_var


request_url = request_url_constructor()

response = requests.get(request_url)

if response.status_code == 200:
    data = response.json()
    if time_series_intraday:
        with open(f'{symbol}_{interval}_api_response.json', 'w') as f:   # CHANGE THE NAME OF THE FILE
            json.dump(data, f)
        print(f'File saved successfully (intraday data)!')
    elif time_series_daily:
        with open(f'{symbol}_D1_api_response.json', 'w') as f:   # CHANGE THE NAME OF THE FILE
            json.dump(data, f)
        print(f'File saved successfully (daily data)!')
else:
    print(f'Error: Unable to fetch data. Status code: {response.status_code}')
