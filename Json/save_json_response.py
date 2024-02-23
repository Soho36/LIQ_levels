import requests
import json
from config import api_key

# api_key = 'DEMO'
# symbol = 'TSLA'
symbol = 'INDO'
# symbol = 'MSFT'
# interval = '5min'

# url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}'
#
# url_intraday = (f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&'
#                 f'interval={interval}&apikey={api_key}')
# url_daily = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'

url_daily_full = (f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&'
                  f'outputsize=full&apikey={api_key}')

response = requests.get(url_daily_full)

if response.status_code == 200:
    data = response.json()
    with open(f'{symbol}_D1_api_response.json', 'w') as f:   # CHANGE THE NAME OF THE FILE
        json.dump(data, f)
else:
    print(f'Error: Unable to fetch data. Status code: {response.status_code}')
