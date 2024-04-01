import pandas as pd
import yfinance as yf
import numpy as np
import mplfinance as mpf


use_csv_or_yf = True                # True for CSV false for YF
plot_candlestick_chart = True       # Plot Chart

symbol = 'NVDA'
history_file_path = 'History_data/MT5/BTCUSD_M5_today.csv'


def get_stock_price(sym):
    if not use_csv_or_yf:
        df = yf.download(sym, start='2024-03-20', end='2024-03-27', interval='15m', progress=False)
        df.index = pd.to_datetime(df.index)
        print(df)
        return df

    elif use_csv_or_yf:
        columns_to_parse = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Filename']
        df = pd.read_csv(history_file_path, parse_dates=[0], dayfirst=False, usecols=columns_to_parse)
        df['Date'] = df['Date'].astype(str)
        df['Time'] = df['Time'].astype(str)
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        df.set_index('Datetime', inplace=True)
        df = df.loc[:, ['Open', 'High', 'Low', 'Close']]
        print(df)
        return df

    else:
        print("At least one must be chosen")


dataframe = get_stock_price(symbol)


def find_levels(dataframe):
    levels_startpoints = []
    levels_endpoints = []

    for i in range(2, len(dataframe) - 2):
        # Support level
        if (dataframe['Low'][i] < dataframe['Low'][i-1]) and \
           (dataframe['Low'][i] < dataframe['Low'][i+1]) and \
           (dataframe['Low'][i+1] < dataframe['Low'][i+2]) and \
           (dataframe['Low'][i-1] < dataframe['Low'][i-2]):
            date_1 = dataframe.index[i]
            price_1 = dataframe['Low'][i]
            date_2 = dataframe.index[-1]
            price_2 = dataframe['Low'][i]
            if not is_near_level(price_1, levels_startpoints, dataframe):
                levels_startpoints.append((date_1, price_1))
                levels_endpoints.append((date_2, price_2))
        # Resistance level
        elif (dataframe['High'][i] > dataframe['High'][i-1]) and \
             (dataframe['High'][i] > dataframe['High'][i+1]) and \
             (dataframe['High'][i+1] > dataframe['High'][i+2]) and \
             (dataframe['High'][i-1] > dataframe['High'][i-2]):
            date_1 = dataframe.index[i]
            price_1 = dataframe['High'][i]
            date_2 = dataframe.index[-1]
            price_2 = dataframe['High'][i]
            if not is_near_level(price_1, levels_startpoints, dataframe):
                levels_startpoints.append((date_1, price_1))
                levels_endpoints.append((date_2, price_2))
    return levels_startpoints, levels_endpoints


def is_near_level(value, levels, df):
    average = np.mean(df['High'] - df['Low'])
    return any(abs(value - level) < average for _, level in levels)


levels_startpoints_to_chart, levels_endpoints_to_chart = find_levels(dataframe)

levels_points = [[a, b] for a, b in zip(levels_startpoints_to_chart, levels_endpoints_to_chart)]


if plot_candlestick_chart:
    def plot_chart(levels, df):
        mpf.plot(df, type='candle', figsize=(12, 6),
                 alines=dict(alines=levels_points, linewidths=2, alpha=0.4), style='yahoo')


    plot_chart(levels_startpoints_to_chart, dataframe)
