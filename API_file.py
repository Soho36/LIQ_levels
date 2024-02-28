import requests
import json
import pandas as pd
from config import api_key
# api_key = 'DEMO'

# *****************************************************************************
data_from_api_from_file = False  # True for Api, False for JSON file # USING only JSON FILES UNTIL NO SUBSCRIPTION

time_series_daily = False
time_series_intraday = True
output_size_full = True

symbol = 'TSLA'

interval = 'Daily'
# interval = '1min'
# interval = '5min'
# interval = '15min'
# interval = '30min'
# interval = '60min'


# ADDED OPTION TO CREATE JSON FILE FOR DEVELOPMENT PURPOSES TO REDUCE API REQUESTS (MEET THE LIMITS)

def request_constructor():

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


request_url = request_constructor()    # Function call


def get_data():

    if data_from_api_from_file:
        response = requests.get(request_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f'Error: Unable to fetch data. Status code: {response.status_code}')
            return None
    else:
        with open(f'Json/{symbol}_{interval}_api_response.json', 'r') as f:
            data = json.load(f)
            return data


json_data_to_dataframe = get_data()


def data_to_dataframe(data):

    # print(data)
    time_series = data[f'Time Series ({interval})']
    dataframe = pd.DataFrame(time_series).T

    dataframe.index = pd.to_datetime(dataframe.index)
    dataframe.sort_index(inplace=True)

    dataframe.reset_index(inplace=True)
    dataframe.rename(columns={'index': 'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low',
                              '4. close': 'Close', '5. volume': 'Volume'}, inplace=True)

    dataframe['Time'] = dataframe['Date'].dt.time   # Adding Time column derived from Datetime
    dataframe['Date'] = dataframe['Date'].dt.date   # # Adding Date column derived from Datetime
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])
    dataframe = dataframe.sort_values(by='Date')    # Sort dataframe by date column
    dataframe.reset_index(drop=True, inplace=True)      # Set numeric indexes

    dataframe['Open'] = pd.to_numeric(dataframe['Open'])    # Convert string to numeric values
    dataframe['High'] = pd.to_numeric(dataframe['High'])
    dataframe['Low'] = pd.to_numeric(dataframe['Low'])
    dataframe['Close'] = pd.to_numeric(dataframe['Close'])
    dataframe['Volume'] = pd.to_numeric(dataframe['Volume'])
    dataframe['Time'] = dataframe['Time'].astype(str)
    dataframe['Symbol'] = symbol
    if __name__ == "__main__":
        print(dataframe)
        print(dataframe.info())
    return dataframe


dataframe_from_api = data_to_dataframe(json_data_to_dataframe)
