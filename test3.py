import pandas as pd
import yfinance as yf
import numpy as np
import mplfinance as mpf
import matplotlib.dates as mpl_dates


use_csv_or_yf = False                # True for CSV false for YF
plot_candlestick_chart = True       # Plot Chart
show_levels = True                 # Plot price levels

symbol = 'NVDA'
history_file_path = 'History_data/MT5/BTCUSD_M5_today.csv'


def get_stock_price(sym):
    if not use_csv_or_yf:
        df = yf.download(sym, start='2024-03-26', end='2024-03-27', interval='5m', progress=False)
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
    levels = []

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
            if not is_near_level(price_1, levels, dataframe):
                levels.append((date_1, price_1, date_2, price_2))
        # Resistance level
        elif (dataframe['High'][i] > dataframe['High'][i-1]) and \
             (dataframe['High'][i] > dataframe['High'][i+1]) and \
             (dataframe['High'][i+1] > dataframe['High'][i+2]) and \
             (dataframe['High'][i-1] > dataframe['High'][i-2]):
            date_1 = dataframe.index[i]
            price_1 = dataframe['High'][i]
            date_2 = dataframe.index[-1]
            price_2 = dataframe['Low'][i]

            if not is_near_level(price_1, levels, dataframe):
                levels.append((date_1, price_1, date_2, price_2))

    return levels


def is_near_level(value, levels, df):
    average = np.mean(df['High'] - df['Low'])
    return any(abs(value - level) < average for _, level in levels)


levels_to_chart = find_levels(dataframe)




if plot_candlestick_chart:
    def plot_chart(levels, df):
        fig, ax = mpf.plot(df, figsize=(12, 6), type='candle', style='yahoo', returnfig=True)

        for timestamp, level_value in levels:
            x_coord = timestamp
            ax[0].axhline(y=level_value, xmin=x_coord / len(dataframe.index), xmax=1, color='blue', linestyle='--')

            # ax[0].axhline(y=level_value, xmin=df['Datetime'][level[0]], xmax=max(df['Date']), color='blue', linestyle='--')
        mpf.show()


    # def plot_all():
    #     fig, ax = plt.subplots()
    #     candlestick_ohlc(ax, df.values, width=0.6, \
    #                      colorup='green', colordown='red', alpha=0.8)
    #     date_format = mpl_dates.DateFormatter('%d %b %Y')
    #     ax.xaxis.set_major_formatter(date_format)
    #     fig.autofmt_xdate()
    #     fig.tight_layout()
    #     for level in levels:
    #         plt.hlines(level[1], xmin=df['Date'][level[0]], \
    #                    xmax=max(df['Date']), colors='blue')
    #     fig.show()

    print('Timestamps and Levels to chart: ', levels_to_chart)
    plot_chart(levels_to_chart, dataframe)
