import pandas as pd
import yfinance as yf
import numpy as np
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt


# fractal

use_csv_or_yf = True    # True for CSV false for YF

symbol = 'msft'
history_file_path = 'History_data/MT5/BTCUSD_M5_today.csv'
columns_to_parse = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Filename']


def get_stock_price(sym):
    df = None
    if not use_csv_or_yf:
        df = yf.download(sym, start='2021-02-01', threads=False)
        df['Date'] = pd.to_datetime(df.index)
        df['Date'] = df['Date'].apply(mpl_dates.date2num)
        df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
        print(df.dtypes)
        print(df[df.isna().any(axis=1)])

    elif use_csv_or_yf:
        df = pd.read_csv(history_file_path, parse_dates=[0], dayfirst=False, usecols=columns_to_parse)
        df['Date'] = pd.to_datetime(df.index)
        df['Date'] = df['Date'].apply(mpl_dates.date2num)
        print(df.dtypes)
        print(df[df.isna().any(axis=1)])

    else:
        print("At least one must be chosen")
    print(df)
    return df


dataframe = get_stock_price(symbol)


def is_support(df, i):
    cond1 = df['Low'][i] < df['Low'][i-1]
    cond2 = df['Low'][i] < df['Low'][i+1]
    cond3 = df['Low'][i+1] < df['Low'][i+2]
    cond4 = df['Low'][i-1] < df['Low'][i-2]
    if cond1 and cond2 and cond3 and cond4:
        return True


def is_resistance(df, i):
    cond1 = df['High'][i] > df['High'][i-1]
    cond2 = df['High'][i] > df['High'][i+1]
    cond3 = df['High'][i+1] > df['High'][i+2]
    cond4 = df['High'][i-1] > df['High'][i-2]
    if cond1 and cond2 and cond3 and cond4:
        return True


def is_far_from_level(value, levels, df):
    ave = np.mean(df['High'] - df['Low'])
    return np.sum([abs(value - level) < ave for _, level in levels]) == 0


def plot_all(levels, df):
    fig, ax = plt.subplots(figsize=(10, 6))
    candlestick_ohlc(ax, df.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax.xaxis.set_major_formatter(date_format)
    for level in levels:
        plt.hlines(level[1], xmin=df['Date'][level[0]], xmax=max(df['Date']), colors='blue', linestyle='--')
    plt.show()


levels = []

for i in range(2, len(dataframe)-2):
    if is_support(dataframe, i):
        l = dataframe['Low'][i]
        if is_far_from_level(l, levels, dataframe):
            levels.append((i, l))
    elif is_resistance(dataframe, i):
        l = dataframe['High'][i]
        if is_far_from_level(l, levels, dataframe):
            levels.append((i, l))

plot_all(levels, dataframe)
