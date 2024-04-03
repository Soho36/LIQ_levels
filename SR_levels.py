import pandas as pd
import yfinance as yf
import numpy as np
import mplfinance as mpf


use_csv_or_yf = False                # True for CSV false for YF
plot_candlestick_chart = True       # Plot Chart

symbol = 'TSLA'
history_file_path = 'History_data/MT5/BTCUSD_M5_today.csv'


def get_stock_price(sym):
    if not use_csv_or_yf:
        df = yf.download(sym, start='2024-03-26', end='2024-03-30', interval='30m', progress=False)
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
    levels_startpoints_tuples = []
    levels_endpoints_tuples = []
    support_levels = []
    resistance_levels = []
    level_discovery_signal = []
    level_discovery_signal.insert(0, None)
    level_discovery_signal.insert(1, None)

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

            if not is_near_level(price_level_1, levels_startpoints_tuples, df):
                levels_startpoints_tuples.append((datetime_1, price_level_1))
                levels_endpoints_tuples.append((datetime_2, price_level_2))
                support_levels.append((datetime_1, price_level_1))
                level_discovery_signal.append(100)
            else:
                level_discovery_signal.append(None)

    # Resistance levels
        elif ((df['High'][i] > df['High'][i - 1]) and
              (df['High'][i] > df['High'][i + 1]) and
              (df['High'][i + 1] > df['High'][i + 2]) and
              (df['High'][i - 1] > df['High'][i - 2])):
            datetime_1 = df.index[i]
            price_level_1 = df['High'][i]
            datetime_2 = df.index[-1]
            price_level_2 = df['High'][i]

            if not is_near_level(price_level_1, levels_startpoints_tuples, df):
                levels_startpoints_tuples.append((datetime_1, price_level_1))
                levels_endpoints_tuples.append((datetime_2, price_level_2))
                resistance_levels.append((datetime_1, price_level_1))
                level_discovery_signal.append(-100)
            else:
                level_discovery_signal.append(None)

        else:
            level_discovery_signal.append(None)

    level_discovery_signal.extend([None, None])   # Appending two elements to the end, to match Dataframe length
    print('Signals list length: ', len(level_discovery_signal))
    level_discovery_signals_series = pd.Series(level_discovery_signal)

    return (levels_startpoints_tuples, levels_endpoints_tuples, support_levels, resistance_levels,
            level_discovery_signal, level_discovery_signals_series)


def is_near_level(value, levels, df):
    average = np.mean(df['High'] - df['Low'])
    return any(abs(value - level) < average for _, level in levels)


(levels_startpoints_to_chart, levels_endpoints_to_chart, support_levels_to, resistance_levels_to, signals_list_to,
 level_discovery_signals_series_to) = find_levels(dataframe)

print('Level series length: ', len(level_discovery_signals_series_to))
print('Level series: \n', level_discovery_signals_series_to)
# print(levels_startpoints_to_chart)

levels_points = [[a, b] for a, b in zip(levels_startpoints_to_chart, levels_endpoints_to_chart)]


def trade_simulation(df, support_levels, resistance_levels):

    resistance_levels = [round(price, 2) for (timestamp, price) in resistance_levels]
    support_levels = [round(price, 2) for (timestamp, price) in support_levels]
    print()
    print('Resistance prices: ', resistance_levels)  # Get list of resistance prices
    print('Support prices: ', support_levels)           # Get list of support prices

    level_rejection_signals_list = []
    level_rejection_signals_list.insert(0, None)
    level_rejection_signals_list.insert(1, None)

    # Support perk finding loop
    level_rejection_signals_list = [None, None]  # Initialize the list with two None values

    # Iterate through each candlestick
    for index in range(2, len(df) - 2):
        support_pierced = False
        resistance_pierced = False

        # Check for support matches
        for s_level in support_levels:
            if df['Low'][index] < s_level:
                if df['Close'][index] > s_level:
                    level_rejection_signals_list.append(100)  # Append support signal
                    # print('Match found for support', index)
                    support_pierced = True
                    break  # Exit the loop once a match is found

        # Check for resistance matches if no support match is found
        for r_level in resistance_levels:
            if df['High'][index] > r_level:
                if df['Close'][index] < r_level:
                    level_rejection_signals_list.append(-100)  # Append resistance signal
                    # print('Match found for resistance', index)
                    resistance_pierced = True
                    break  # Exit the loop once a match is found

        # If neither support nor resistance match is found, append None
        if not support_pierced and not resistance_pierced:
            level_rejection_signals_list.append(None)

    level_rejection_signals_list.extend([None, None])

    level_rejection_signals_list_series = pd.Series(level_rejection_signals_list)
    print(level_rejection_signals_list_series)

    return level_rejection_signals_list_series


level_rejection_signals_list_series_to = trade_simulation(dataframe, support_levels_to, resistance_levels_to)


# Print Candlestick Chart
if plot_candlestick_chart:

    def plot_chart(df, level_discovery_signals_series, level_rejection_signals_list_series):
        plots_list = []

        for i, s in enumerate(level_discovery_signals_series):
            if s != 'NaN':
                plots_list.append(mpf.make_addplot(level_discovery_signals_series, type='scatter', color='black',
                                                   markersize=250, marker='*', panel=1))
        for i, s in enumerate(level_rejection_signals_list_series):
            if s != 'NaN':
                plots_list.append(mpf.make_addplot(level_rejection_signals_list_series, type='scatter', color='black',
                                                   markersize=250, marker='+', panel=1))

        mpf.plot(df, type='candle', figsize=(12, 6),
                 alines=dict(alines=levels_points, linewidths=2, alpha=0.4), style='yahoo', addplot=plots_list)


    plot_chart(dataframe, level_discovery_signals_series_to, level_rejection_signals_list_series_to)
