import pandas as pd
import yfinance as yf
import numpy as np
import mplfinance as mpf


use_csv_or_yf = False                # True for CSV false for YF
plot_candlestick_chart = False       # Plot Chart

symbol = 'TSLA'
history_file_path = 'History_data/MT5/BTCUSD_M5_today.csv'


def get_stock_price(sym):
    if not use_csv_or_yf:
        df = yf.download(sym, start='2024-03-01', end='2024-03-02', interval='60m', progress=False)
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

    level_discovery_signal_to_chart = []
    level_discovery_signal_to_chart.insert(0, None)
    level_discovery_signal_to_chart.insert(1, None)

    support_levels_running_state = []
    support_levels_running_state.insert(0, None)
    support_levels_running_state.insert(1, None)

    resistance_levels_running_state = []
    resistance_levels_running_state.insert(0, None)
    resistance_levels_running_state.insert(1, None)

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

                support_levels_running_state.append(price_level_1)
                level_discovery_signal_to_chart.append(100)
                resistance_levels_running_state.append(None)
            else:
                support_levels_running_state.append(None)
                resistance_levels_running_state.append(None)
                level_discovery_signal_to_chart.append(None)

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

                resistance_levels_running_state.append(price_level_1)
                level_discovery_signal_to_chart.append(-100)
                support_levels_running_state.append(None)
            else:
                resistance_levels_running_state.append(None)
                support_levels_running_state.append(None)
                level_discovery_signal_to_chart.append(None)

        else:
            level_discovery_signal_to_chart.append(None)
            support_levels_running_state.append(None)
            resistance_levels_running_state.append(None)

    level_discovery_signal_to_chart.extend([None, None])   # Appending two elements to the end, to match Dataframe length
    support_levels_running_state.extend([None, None])
    resistance_levels_running_state.extend([None, None])

    level_discovery_signals_series = pd.Series(level_discovery_signal_to_chart)

    return (levels_startpoints_tuples, levels_endpoints_tuples, support_levels_running_state,
            resistance_levels_running_state, level_discovery_signals_series, level_discovery_signal_to_chart)


def is_near_level(value, levels, df):
    average = np.mean(df['High'] - df['Low'])
    return any(abs(value - level) < average for _, level in levels)


(levels_startpoints_to_chart, levels_endpoints_to_chart, support_level_signal_running_out,
 resistance_level_signal_running_out, level_discovery_signals_series_out, level_discovery_signal_to_chart_out) = (
    find_levels(dataframe))

# ww = print('Sig', list(enumerate(level_discovery_signal_to_chart_out)))
# ii = print('Sup', list(enumerate(support_level_signal_running_out)))
# ee = print('Res', list(enumerate(resistance_level_signal_running_out)))

print(level_discovery_signal_to_chart_out)
print(support_level_signal_running_out)
print(resistance_level_signal_running_out)


levels_points = [[a, b] for a, b in zip(levels_startpoints_to_chart, levels_endpoints_to_chart)]


# THIS PART SEARCHING FOR LEVEL REJECTION
def trade_simulation(df, support_levels_running, resistance_levels_running):

    # resistance_levels = [round(price, 2) for (timestamp, price) in resistance_levels]
    # support_levels = [round(price, 2) for (timestamp, price) in support_levels]
    print()

    # Initialize the list with two None values
    level_rejection_signals_list = []
    # level_rejection_signals_list.insert(0, None)
    # level_rejection_signals_list.insert(1, None)

    # Support rejection finding loop
    # Iterate through each candlestick
    for index in range(2, len(df) - 2):
        support_pierced = False
        resistance_pierced = False

        # Check for support rejection
        for ss_level in support_levels_running:
            if ss_level is not None:
                if df['Low'][index] < ss_level:
                    if df['Close'][index] > ss_level:
                        level_rejection_signals_list.append(100)  # Append support signal
                        # print('Match found for support', index)
                        support_pierced = True
                        break  # Exit the loop once a match is found
            # level_rejection_signals_list.append(None)
            # break
        # Check for resistance matches if no support match is found
        for rr_level in resistance_levels_running:
            if rr_level is not None:
                if df['High'][index] > rr_level:
                    if df['Close'][index] < rr_level:
                        level_rejection_signals_list.append(-100)  # Append resistance signal
                        # print('Match found for resistance', index)
                        resistance_pierced = True
                        break  # Exit the loop once a match is found
            # level_rejection_signals_list.append(None)
            # break
        # If neither support nor resistance match is found, append None
        if not support_pierced and not resistance_pierced:
            level_rejection_signals_list.append(None)

    # level_rejection_signals_list.extend([None, None])

    level_rejection_signals_series = pd.Series(level_rejection_signals_list)

    return level_rejection_signals_series


level_rejection_signals_series_from_trade_simulation = trade_simulation(dataframe, support_level_signal_running_out,
                                                                        resistance_level_signal_running_out)


# PRINT CANDLESTICK CHART WITH LEVELS AND SIGNALS AS ADDITIONAL PLOT
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


    plot_chart(dataframe, level_discovery_signals_series_out, level_rejection_signals_series_from_trade_simulation)
