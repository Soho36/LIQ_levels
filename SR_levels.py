import pandas as pd
import yfinance as yf
import numpy as np
import mplfinance as mpf


use_csv_or_yf = False                # True for CSV false for YF
plot_candlestick_chart = True       # Plot Chart

symbol = 'NVDA'
history_file_path = 'History_data/MT5/BTCUSD_M5_today.csv'


def get_stock_price(sym):
    if not use_csv_or_yf:
        df = yf.download(sym, start='2024-03-20', end='2024-03-21', interval='5m', progress=False)
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


def find_levels(df):
    levels_startpoints = []
    levels_endpoints = []
    support_levels = []
    resistance_levels = []
    signals_list = []
    signals_list.insert(0, None)
    signals_list.insert(1, None)

    # Support levels
    for i in range(2, len(df) - 2):
        if (df['Low'][i] < df['Low'][i - 1]) and \
           (df['Low'][i] < df['Low'][i + 1]) and \
           (df['Low'][i + 1] < df['Low'][i + 2]) and \
           (df['Low'][i - 1] < df['Low'][i - 2]):
            datetime_1 = df.index[i]
            price_level_1 = df['Low'][i]
            datetime_2 = df.index[-1]
            price_level_2 = df['Low'][i]

            if not is_near_level(price_level_1, levels_startpoints, df):
                levels_startpoints.append((datetime_1, price_level_1))
                levels_endpoints.append((datetime_2, price_level_2))
                support_levels.append((datetime_1, price_level_1))
                signals_list.append(100)
            else:
                signals_list.append(None)

    # Resistance levels
        elif ((df['High'][i] > df['High'][i - 1]) and
              (df['High'][i] > df['High'][i + 1]) and
              (df['High'][i + 1] > df['High'][i + 2]) and
              (df['High'][i - 1] > df['High'][i - 2])):
            datetime_1 = df.index[i]
            price_level_1 = df['High'][i]
            datetime_2 = df.index[-1]
            price_level_2 = df['High'][i]

            if not is_near_level(price_level_1, levels_startpoints, df):
                levels_startpoints.append((datetime_1, price_level_1))
                levels_endpoints.append((datetime_2, price_level_2))
                resistance_levels.append((datetime_1, price_level_1))
                signals_list.append(-100)
            else:
                signals_list.append(None)

        else:
            signals_list.append(None)

    signals_list.extend([None, None])   # Appending two elements to the end, to match Dataframe length
    print('Signals list length: ', len(signals_list))
    level_reject_signals_series = pd.Series(signals_list)

    return (levels_startpoints, levels_endpoints, support_levels, resistance_levels,
            signals_list, level_reject_signals_series)


def is_near_level(value, levels, df):
    average = np.mean(df['High'] - df['Low'])
    return any(abs(value - level) < average for _, level in levels)


(levels_startpoints_to_chart, levels_endpoints_to_chart, support_levels_to, resistance_levels_to, signals_list_to,
 level_reject_signals_series_to) = find_levels(dataframe)

print('Signals series length: ', len(level_reject_signals_series_to))
print('Signal series: \n', level_reject_signals_series_to)
print(levels_startpoints_to_chart)

levels_points = [[a, b] for a, b in zip(levels_startpoints_to_chart, levels_endpoints_to_chart)]


def trade_simulation(df, support_levels, resistance_levels):

    resistance_prices = [round(price, 2) for (timestamp, price) in resistance_levels]
    support_prices = [round(price, 2) for (timestamp, price) in support_levels]

    print('Resistance prices: ', resistance_prices)  # Get list of resistance prices
    print('Support prices: ', support_prices)           # Get list of support prices

    # Support perk finding loop
    for i in range(2, len(df) - 2):
        for e in support_prices:
            if df['Low'][i] < e:
                if df['Close'][i] > e:
                    print('Match found for support', i)

    for i in range(2, len(df) - 2):
        for e in resistance_prices:
            if df['High'][i] > e:
                if df['Close'][i] < e:
                    print('Match found resistance', i)


trade_simulation(dataframe, support_levels_to, resistance_levels_to)


# Print Candlestick Chart
if plot_candlestick_chart:

    def plot_chart(df, level_reject_signals_series):
        plots_list = []

        for i, s in enumerate(level_reject_signals_series):
            if s != 'NaN':
                plots_list.append(mpf.make_addplot(level_reject_signals_series, type='scatter', color='black',
                                                   markersize=250, marker='+', panel=1))

        mpf.plot(df, type='candle', figsize=(12, 6),
                 alines=dict(alines=levels_points, linewidths=2, alpha=0.4), style='yahoo', addplot=plots_list)


    plot_chart(dataframe, level_reject_signals_series_to)
