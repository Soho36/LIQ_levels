import requests
from config import api_key       # use this for limited response

# api_key = 'DEMO'    # use this to get demo response

symbol = 'TSLA'
# symbol = 'NVDA'


interval = 'Daily'
# interval = '1min'
# interval = '5min'
# interval = '15min'
# interval = '30min'
# interval = '60min'

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLA&interval=5min&apikey=YOUR_API_KEY'

url_intraday = (f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&'
                f'interval={interval}&apikey={api_key}')
url_daily = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'

url_daily_full = (f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&'
                  f'outputsize=full&apikey={api_key}')

response = requests.get(url_daily_full)
print(response)

if response.status_code == 200:
    html_content = response.text
    print(html_content)
    with open('webpage.html', 'w', encoding='utf-8') as f:      # CHANGE TO DEFAULT NAME AFTER CREATING
        f.write(html_content)
else:
    print(f'Error: Unable to fetch webpage. Status code: {response.status_code}')
