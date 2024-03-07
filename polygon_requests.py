import requests
import json
import pandas as pd
from config import api_key_polygon

ticker = 'AAPL'             # Case-sensitive ticker symbol
multiplier = 5              # Timespan multiplier
timespan = 'minute'            # Time window (day, minute)
from_date = '2024-03-06'
to_date = '2024-03-07'
adjusted = 'true'           # Whether the results are adjusted for splits
sort = 'asc'                # asc will return oldest at the top, desc newest at the top
limit = 5000                # Default 5000 and Max 50000

request_url = (
    f'https://api.polygon.io/v2/aggs/'
    f'ticker/{ticker}/range/{multiplier}/{timespan}/'
    f'{from_date}/{to_date}?adjusted={adjusted}&sort={sort}&limit={limit}&'
    f'apiKey={api_key_polygon}'
)


def get_data():
    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Error: Unable to fetch data. Status code: {response.status_code}')
        return None


json_data_to_dataframe = get_data()

print(json_data_to_dataframe)


def data_to_dataframe(data):
    dataframe = pd.DataFrame(data)
    if 'results' in dataframe.columns:
        for result in dataframe['results']:
            result['t'] = pd.to_datetime(result['t'], unit='ms')

        dataframe['t'] = pd.to_datetime(dataframe['results'].apply(lambda x: x['t']), unit='ms')  # Convert to datetime
        dataframe.drop(columns='results', inplace=True)

        return dataframe
    else:
        print('Column results not found in DataFrame')


dataframe_from_api = data_to_dataframe(json_data_to_dataframe)

print(dataframe_from_api)
