import pandas as pd
import yfinance as yf
import numpy as np
import mplfinance as mpf


use_csv_or_yf = True                # True for CSV false for YF
plot_candlestick_chart = True       # Plot Chart

symbol = 'TSLA'
history_file_path = 'History_data/MT5/BTCUSD_M5_today.csv'


def get_stock_price(sym):
    if not use_csv_or_yf:
        df = yf.download(sym, start='2024-03-28', end='2024-03-28', interval='5m', progress=False)
        df.index = pd.to_datetime(df.index)
        print('Dataframe: \n', df)
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


# SEARCH FOR LEVELS
def find_levels(df):
    levels_startpoints_tuples = []
    levels_endpoints_tuples = []

    level_discovery_signal = []
    level_discovery_signal.insert(0, None)
    level_discovery_signal.insert(1, None)

    sr_levels = []
    support_levels = []
    resistance_levels = []

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

                sr_levels.append(price_level_1)  # SR levels
                support_levels.append(price_level_1)
                level_discovery_signal.append(0)
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

                sr_levels.append(price_level_1)  # SR levels
                resistance_levels.append(price_level_1)
                level_discovery_signal.append(0)
            else:
                level_discovery_signal.append(None)

        else:
            level_discovery_signal.append(None)

    level_discovery_signal.extend([None, None])  # Appending two elements to the end, to match Dataframe length

    print('level_discovery_signal: \n', level_discovery_signal)
    level_discovery_signals_series = pd.Series(level_discovery_signal)
    # level_discovery_signals_series.index = df['Date']

    return (levels_startpoints_tuples, levels_endpoints_tuples, support_levels,
            resistance_levels, level_discovery_signals_series, sr_levels)


def is_near_level(value, levels, df):
    average = np.mean(df['High'] - df['Low'])
    return any(abs(value - level) < average for _, level in levels)


(levels_startpoints_to_chart, levels_endpoints_to_chart, support_level_signal_running_out,
 resistance_level_signal_running_out, level_discovery_signals_series_out,
 sr_levels_out) = find_levels(dataframe)


print('Support level: \n', support_level_signal_running_out)
print('Resistance level: \n', resistance_level_signal_running_out)
print('SR levels: \n', sr_levels_out)


levels_points = [[a, b] for a, b in zip(levels_startpoints_to_chart, levels_endpoints_to_chart)]
print('levels_points', levels_points)

# *********************************************************************************************************************
# THIS PART SEARCHING FOR LEVEL REJECTION


def level_rejection_signals(df, sr_levels, level_discovery_signals_series):

    crossing_signals = []
    df.reset_index(inplace=True)
    discovered = False                              # Flag to track if a level was discovered
    for index, row in df.iterrows():
        if pd.notna(level_discovery_signals_series[index]):
            discovered = True                       # Set the flag if level was discovered
        if discovered:
            previous_close = df.iloc[index - 1]['Close']
            current_candle_close = row['Close']
            current_candle_high = row['High']
            current_candle_low = row['Low']

            signal = None

            for level in sr_levels:

                if previous_close < level:      # Check if the previous close was below the resistance level
                    if current_candle_high > level:     # Price has crossed above resistance level
                        if current_candle_close < level:    # but closed below
                            signal = -100
                            break

                elif previous_close > level:    # Check if the previous close was above the support level
                    if current_candle_low < level:      # Price has crossed below support level
                        if current_candle_close > level:    # but closed above
                            signal = 100
                            break
            crossing_signals.append(signal)

        else:
            crossing_signals.append(None)   # Append None for indices before discovery

    print('Crossing_signals: ', crossing_signals)
    crossing_signals_series = pd.Series(crossing_signals)
    return crossing_signals_series


crossing_signals_series_outside = level_rejection_signals(dataframe, sr_levels_out, level_discovery_signals_series_out)
print('Crossing_signals_series: \n', crossing_signals_series_outside)
print('Level_discovery_signals: \n', level_discovery_signals_series_out)

# ******************************************************************************************************
# PRINT CANDLESTICK CHART WITH LEVELS AND SIGNALS AS ADDITIONAL PLOT
if plot_candlestick_chart:

    def plot_chart(df, level_discovery_signals_series, crossing_signals_series):

        df.set_index('Datetime', inplace=True)
        plots_list = []

        for i, s in enumerate(level_discovery_signals_series):
            if s != 'NaN':
                plots_list.append(mpf.make_addplot(level_discovery_signals_series, type='scatter', color='black',
                                                   markersize=250, marker='*', panel=1))
        for i, s in enumerate(crossing_signals_series):
            if s != 'NaN':
                plots_list.append(mpf.make_addplot(crossing_signals_series, type='scatter', color='black',
                                                   markersize=250, marker='+', panel=1))

        mpf.plot(df, type='candle', figsize=(12, 6),
                 alines=dict(alines=levels_points, linewidths=2, alpha=0.4), style='yahoo', addplot=plots_list)


    plot_chart(dataframe, level_discovery_signals_series_out, crossing_signals_series_outside)
