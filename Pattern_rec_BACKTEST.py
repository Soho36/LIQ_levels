import talib
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import statistics
from API_or_Json import dataframe_from_api


# ------------------------------------------
# The list of paths to datafiles:
# file_path = 'History_data/merged_data.csv'
# file_path = 'History_data/exel.csv'
# file_path = 'History_data/spr.csv'
# file_path = 'History_data/zim.csv'
# file_path = 'History_data/extr.csv'
# file_path = 'History_data/aehr.csv'
# file_path = 'History_data/tsla_D1.csv'
# file_path = 'History_data/neog_D1.csv'
# file_path = 'History_data/meta_D1.csv'
# file_path = 'History_data/tsla_m5.csv'
# file_path = 'History_data/STOCKS/tsla_m1.csv'
# file_path = 'History_data/MT4/BTCUSD_D1.csv'
# file_path = 'History_data/MT4/BTCUSD_m60.csv'
# file_path = 'History_data/MT4/BTCUSD_m5.csv'
# file_path = 'History_data/MT4/BTCUSD1.csv'

# file_path = 'History_data/MT5/BTCUSD_M5.csv'
# file_path = 'History_data/MT5/BTCUSD_M1.csv'
# file_path = 'History_data/MT5/BTCUSD_M1_4_years.csv'
# file_path = 'History_data/MT5/BTCUSD_M30.csv'
# file_path = 'History_data/MT5/BTCUSD_H1.csv'
# file_path = 'History_data/MT5/BTCUSD_D1.csv'
# file_path = 'History_data/MT5/BTCUSD_H4.csv'
# file_path = 'History_data/MT5/BTCUSD_H4.csv'
file_path = 'History_data/MT5/BTCUSD_M15.csv'
# file_path = 'History_data/MT5/BTCUSD_M5_today.csv'
# file_path = 'History_data/MT5/BTCUSD_M30_today.csv'
# file_path = 'History_data/MT5/BTCUSD_M15_today.csv'
# ------------------------------------------
# pd.set_option('display.max_columns', 10)  # Uncomment to display all columns


# **************************************** SETTINGS **************************************
# symbol = 'TSLA'
dataframe_source_api_or_csv = False    # True for API or response file, False for CSV
start_date = '2023-04-03'       # Choose the start date to begin from
end_date = '2023-04-03'         # Choose the end date

# SIMULATION
start_simulation = True
show_trade_analysis = True

# ENTRY CONDITIONS
use_find_levels = True
use_level_rejection = True
use_level_rejection_entry = False
#
number_of_pattern = 4          # Choose the index of pattern (from Ta-lib patterns.csv)
use_pattern_recognition = False
#
use_piercing_signal = False
longs_allowed = True            # Allow or disallow trade direction
shorts_allowed = True          # Allow or disallow trade direction

# RISK MANAGEMENT

spread = 0
risk_reward_ratio = 1   # Chose risk/reward ratio (aiming to win compared to lose)
stop_loss_as_candle_min_max = True  # Must be True if next condition is false
stop_loss_offset = 10                 # Is added to SL for Shorts and subtracted for Longs (can be equal to spread)

stop_loss_as_plus_candle = False    # Must be True if previous condition is false
stop_loss_offset_multiplier = 15    # 1 places stop one candle away from H/L (only when stop_loss_as_plus_candle = True

stop_loss_price_as_dollar_amount = True     # STOP as distance from entry price
rr_dollar_amount = 100                       # Value for stop as distance


# CHARTS
show_candlestick_chart = True
find_level_rejection_signals = True
show_level_rejection_signals = True
show_line_chart = False
show_signal_line_chart = False
show_profits_losses_line_chart = False  # Only when Simulation is True
show_balance_change_line_chart = True   # Only when Simulation is True


# SIGNALS
sr_levels_timeframe = 30
show_swing_highs_lows = False
print_settings = False

# ******************************************************************************

if print_settings:
    def print_settings():
        print('************************************ SETTINGS ************************************')
        print()
        print(f'dataframe_source_api_or_csv: {dataframe_source_api_or_csv}')
        print(f'start_date: {start_date}')
        print(f'end_date: {end_date}')
        print()
        print('ENTRY CONDITIONS')
        print(f'code_of_pattern: {number_of_pattern}')
        print(f'use_pattern_recognition: {use_pattern_recognition}')
        print(f'use_piercing_signal: {use_piercing_signal}')
        print()
        print('RISK MANAGEMENT')
        print(f'risk_reward_ratio: {risk_reward_ratio}')
        print(f'stop_loss_as_candle_min_max: {stop_loss_as_candle_min_max}')
        print(f'stop_loss_as_plus_candle: {stop_loss_as_plus_candle}')
        print(f'stop_loss_offset_multiplier: {stop_loss_offset_multiplier}')
        print()
        print('SIMULATION')
        print(f'start_simulation: {start_simulation}')
        print(f'show_trade_analysis: {show_trade_analysis}')
        print()
        print('CHARTS')
        print(f'show_candlestick_chart: {show_candlestick_chart}')
        print(f'show_line_chart: {show_line_chart}')
        print(f'show_signal_line_chart: {show_signal_line_chart}')
        print(f'show_profits_losses_line_chart: {show_profits_losses_line_chart}')
        print(f'show_balance_change_line_chart: {show_balance_change_line_chart}')
        print()
        print('SIGNALS')
        print(f'sr_levels_timeframe: {sr_levels_timeframe}')
        print(f'show_swing_highs_lows: {show_swing_highs_lows}')
        # print(f'show_patterns_signals: {show_patterns_signals}')
        # print(f'show_level_pierce_signals: {show_level_pierce_signals}')


    print_settings()


def getting_dataframe_from_file(path):

    # directory_path = 'TXT/'
    print()
    # print('Datafiles in folder: ')
    # for filename in os.listdir(directory_path):     # Making a list of files located in TXT folder
    #     print(filename)
    # print()
    # print(f'Current file is: {path}')

    columns_to_parse = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Filename']

    #  for MT4 files set dayfirst=False
    csv_df = pd.read_csv(path, parse_dates=[0], dayfirst=False, usecols=columns_to_parse)
    print()
    if dataframe_source_api_or_csv is False:
        print(f'Dataframe derived from CSV:\n {csv_df}')
    else:
        pass
    print()
    return csv_df


dataframe_from_csv = getting_dataframe_from_file(file_path)


def date_range_func(df_csv, df_api, start, end):

    date_range = pd.date_range(start=start, end=end, freq='D')
    # print('Date range: \n', list(date_range))

    if dataframe_source_api_or_csv:
        df = df_api
        ticker = df['Symbol'].iloc[0]
        print(ticker)
        print(f'Dataframe derived from API:\n {df}', )
    else:
        df = df_csv
        ticker = df['Filename'].iloc[0]
    date_column = df['Date']        # Select the 'Date' column from the DataFrame
    dates_in_range = date_column.isin(date_range)   # checks which dates from date_column fall within the generated
    # date range, resulting in a boolean mask
    df_filtered_by_date = df[dates_in_range]

    if df_filtered_by_date.empty:
        # print('NB! Dataframe is empty, check the date range!')
        raise ValueError('NB! Dataframe is empty, check the date range!')
    else:
        return ticker, df_filtered_by_date


ticker_name, filtered_by_date_dataframe = date_range_func(dataframe_from_csv, dataframe_from_api, start_date, end_date)

# Make a copy of the original DataFrame
filtered_by_date_dataframe_original = filtered_by_date_dataframe.copy()

print()
print(f'Dataframe filtered by date:\n {filtered_by_date_dataframe}')
print()
print('************************************ TRADES SIMULATION ************************************')

#  ----------------------------------------------------------------------------------------------
#  LEVELS SEARCHING
#  ----------------------------------------------------------------------------------------------

filtered_by_date_dataframe = (filtered_by_date_dataframe.assign(
    Datetime=(filtered_by_date_dataframe['Date'] + pd.to_timedelta(filtered_by_date_dataframe['Time']))))
filtered_by_date_dataframe.set_index('Datetime', inplace=True)
filtered_by_date_dataframe = filtered_by_date_dataframe.loc[:, ['Open', 'High', 'Low', 'Close']]


if use_find_levels:
    def find_levels(filtered_df):
        # print('!!!!!', filtered_df)

        levels_startpoints_tuples = []
        levels_endpoints_tuples = []

        level_discovery_signal = []
        level_discovery_signal.insert(0, None)
        level_discovery_signal.insert(1, None)

        support_levels = []
        resistance_levels = []
        sr_levels = []

        # Support levels
        for i in range(2, len(filtered_df) - 2):
            if (filtered_df['Low'][i] < filtered_df['Low'][i - 1]) and \
               (filtered_df['Low'][i] < filtered_df['Low'][i + 1]) and \
               (filtered_df['Low'][i + 1] < filtered_df['Low'][i + 2]) and \
               (filtered_df['Low'][i - 1] < filtered_df['Low'][i - 2]):
                datetime_1 = filtered_df.index[i]
                price_level_1 = filtered_df['Low'][i]
                datetime_2 = filtered_df.index[-1]
                price_level_2 = filtered_df['Low'][i]

                if not is_near_level(price_level_1, levels_startpoints_tuples, filtered_df):
                    levels_startpoints_tuples.append((datetime_1, price_level_1))
                    levels_endpoints_tuples.append((datetime_2, price_level_2))
                    support_levels.append(price_level_1)
                    level_discovery_signal.append(0)
                    sr_levels.append((i, price_level_1))  # SR levels

                else:
                    level_discovery_signal.append(None)

            # Resistance levels
            elif ((filtered_df['High'][i] > filtered_df['High'][i - 1]) and
                  (filtered_df['High'][i] > filtered_df['High'][i + 1]) and
                  (filtered_df['High'][i + 1] > filtered_df['High'][i + 2]) and
                  (filtered_df['High'][i - 1] > filtered_df['High'][i - 2])):
                datetime_1 = filtered_df.index[i]
                price_level_1 = filtered_df['High'][i]
                datetime_2 = filtered_df.index[-1]
                price_level_2 = filtered_df['High'][i]

                if not is_near_level(price_level_1, levels_startpoints_tuples, filtered_df):
                    levels_startpoints_tuples.append((datetime_1, price_level_1))
                    levels_endpoints_tuples.append((datetime_2, price_level_2))
                    resistance_levels.append(price_level_1)
                    level_discovery_signal.append(0)
                    sr_levels.append((i, price_level_1))  # SR levels
                else:
                    level_discovery_signal.append(None)

            else:
                level_discovery_signal.append(None)

        level_discovery_signal.extend([None, None])  # Appending two elements to the end, to match Dataframe length

        # print('level_discovery_signal: \n', level_discovery_signal)
        level_discovery_signals_series = pd.Series(level_discovery_signal)
        # level_discovery_signals_series.index = df['Date']

        return (levels_startpoints_tuples, levels_endpoints_tuples, support_levels,
                resistance_levels, level_discovery_signals_series, sr_levels)


    def is_near_level(value, levels, df):
        average = np.mean(df['High'] - df['Low'])
        return any(abs(value - level) < average for _, level in levels)


    (levels_startpoints_to_chart, levels_endpoints_to_chart, support_level_signal_running_out,
     resistance_level_signal_running_out, level_discovery_signals_series_out,
     sr_levels_out) = find_levels(filtered_by_date_dataframe)

    # print('Support level: \n', support_level_signal_running_out)
    # print('Resistance level: \n', resistance_level_signal_running_out)
    # print('SR levels: \n', sr_levels_out)

    levels_points_for_chart = [[a, b] for a, b in zip(levels_startpoints_to_chart, levels_endpoints_to_chart)]
    # print('levels_points', levels_points)

else:
    sr_levels_out = []                          # Initialize sr_levels_out with an empty list to avoid warning
    level_discovery_signals_series_out = []     # Initialize sr_levels_out with an empty list to avoid warning

# ********************************************************************************************************************
filtered_by_date_dataframe.reset_index(inplace=True)
print('SR_levels_out: \n', sr_levels_out)
# print('444', len(sr_levels_out))


def add_levels_columns_to_dataframe(df):
    # Initialize counters for columns for 5 levels as a dictionary
    n = 1
    column_counters = {}
    while n < (len(sr_levels_out) + 1):
        column_counters[n] = 0
        n += 1
    # print(column_counters)

    # Loop through the price levels
    for idx, price in sr_levels_out:
        # Determine which column to assign the price level to
        column_number = min(column_counters, key=column_counters.get)
        # Update the DataFrame with the price level
        df.loc[idx, column_number] = price
        # Increment the counter for the assigned column
        column_counters[column_number] += 1

    return column_counters


column_counters_outside = add_levels_columns_to_dataframe(filtered_by_date_dataframe)


def fill_column_with_first_non_null_value(df, column_idx):

    # Check if any non-null value exists in the column
    if not df[column_idx].isna().all():
        # Get the first non-null value
        value_to_fill = df[column_idx].dropna().iloc[0]

        # Find the index of the first occurrence of the non-null value
        start_index = df.loc[df[column_idx] == value_to_fill].index[0]

        # Iterate through the DataFrame and fill the values with the non-null value
        for idx, val in df.iterrows():
            if idx >= start_index:
                df.loc[idx, column_idx] = value_to_fill


# Fill each column with the first non-null value
for column_index in range(1, len(column_counters_outside) + 1):
    fill_column_with_first_non_null_value(filtered_by_date_dataframe, column_index)

filtered_by_date_dataframe.set_index('Datetime', inplace=True)
print(filtered_by_date_dataframe)

# *******************************************************************************************************************
#  ----------------------------------------------------------------------------------------------
#  LEVEL REJECTION SIGNALS
#  ----------------------------------------------------------------------------------------------


if use_find_levels and use_level_rejection:

    def level_rejection_signals(df):

        rejection_signals = []
        df.reset_index(inplace=True)

        for index, row in df.iterrows():
            previous_close = df.iloc[index - 1]['Close']
            current_candle_close = row['Close']
            current_candle_high = row['High']
            current_candle_low = row['Low']

            signal = None  # Reset signal for each row

            for level_column in range(1, len(sr_levels_out) + 1):
                current_sr_level = row[level_column]
                if current_sr_level is not None:
                    if previous_close < current_sr_level:   # Check if the previous close was below the resistance level
                        if current_candle_high > current_sr_level:    # Price has crossed above resistance level
                            signal = -100
                            break
                            # if current_candle_close < current_sr_level:  # but closed below
                            #     signal = -100
                            #     break

                    elif previous_close > current_sr_level:   # Check if the previous close was above the support level
                        if current_candle_low < current_sr_level:    # Price has crossed below support level
                            signal = 100
                            break
                            # if current_candle_close > current_sr_level:  # but closed above
                            #     signal = 100
                            #     break

            rejection_signals.append(signal)

        # print('Rejection_signals: ', rejection_signals)
        rejection_signals_series = pd.Series(rejection_signals)
        return rejection_signals_series


    rejection_signals_series_outside = level_rejection_signals(filtered_by_date_dataframe)


    # print('Rejection_signals_series: \n', rejection_signals_series_outside)
    # print('Level_discovery_signals: \n', level_discovery_signals_series_out)
    filtered_by_date_dataframe.set_index('Datetime', inplace=True)  # Set index back to Datetime
else:
    rejection_signals_series_outside = None  # When function switched off


#  ----------------------------------------------------------------------------------------------
#  PATTERN RECOGNITION
#  ----------------------------------------------------------------------------------------------

patterns_dataframe = pd.read_csv('Ta-lib patterns.csv')


def pattern_recognition(patterns_df, pattern_number):  # Reading Pattern codes from CSV

    if use_pattern_recognition:
        pattern_code = patterns_df['PatternCode'].iloc[pattern_number]
        pattern_name = patterns_df['PatternName'].iloc[pattern_number]
        pattern_index = patterns_df.index[pattern_number]
        active_pattern = {'Pattern_code': pattern_code,
                          'Pattern_name': pattern_name,
                          'Pattern_index': pattern_index}
        print()
        print(f'Current Pattern is: {pattern_code}, {pattern_name}, {pattern_index}')

        pattern_function = getattr(talib, pattern_code)
        # filtered_by_date_dataframe.reset_index(drop=True, inplace=True)
        pattern_signal = pattern_function(filtered_by_date_dataframe['Open'], filtered_by_date_dataframe['High'],
                                          filtered_by_date_dataframe['Low'], filtered_by_date_dataframe['Close'])
        print('Pattern signals searching is ON')
        print(f'Pattern signals: {list(pattern_signal)}')
        return pattern_signal, active_pattern

    else:
        print('Pattern recognition is turned OFF')
        return None, None


# Returns series
pattern_signal_series_outside, active_pattern_list = pattern_recognition(patterns_dataframe, number_of_pattern)
# print('recognized_pattern_signal', pattern_signal_series_outside)


def level_peirce_recognition():

    if use_piercing_signal:
        swing_highs = talib.MAX(filtered_by_date_dataframe['High'], sr_levels_timeframe)
        swing_lows = talib.MIN(filtered_by_date_dataframe['Low'], sr_levels_timeframe)

        filtered_by_date_dataframe.reset_index(drop=True, inplace=True)
        swing_highs.reset_index(drop=True, inplace=True)
        swing_lows.reset_index(drop=True, inplace=True)
        pierce_signals = []

        for i in range(1, len(filtered_by_date_dataframe)):

            # Append -100 if signal discovered for short signal
            if filtered_by_date_dataframe['High'][i] > swing_highs[i - 1]:
                if filtered_by_date_dataframe['Close'][i] < swing_highs[i - 1]:
                    pierce_signals.append(-100)  # Append -100 if signal is discovered
                else:
                    pierce_signals.append(0)

            # Append 100 if signal discovered for long signal
            elif filtered_by_date_dataframe['Low'][i] < swing_lows[i - 1]:
                if filtered_by_date_dataframe['Close'][i] > swing_lows[i - 1]:
                    pierce_signals.append(100)
                else:
                    pierce_signals.append(0)
            else:
                pierce_signals.append(0)
        pierce_signals.insert(0, 0)
        pierce_signals_series = pd.Series(pierce_signals)

        # filtered_by_date_dataframe['Signal'] = pd.Series(signals, index=filtered_by_date_dataframe.index)
        print('Pierce signals searching is ON')
        print(f'Pierce signals: {pierce_signals}')
        # print('Dataframe len ', len(filtered_by_date_dataframe))
        return pierce_signals_series

    else:
        print('Pierce recognition is turned OFF')
        return None


pierce_signals_series_outside = level_peirce_recognition()


#  ----------------------------------------------
#  TRADES SIMULATION
#  ----------------------------------------------

def trades_simulation(filtered_df_original, risk_reward_simulation, sl_offset_multiplier):
    # print('!!!!', filtered_df_original)
    if start_simulation:
        trades_counter = 0
        trade_result_both = []
        trade_result = []
        trade_result_longs = []
        trade_result_shorts = []
        trade_direction = []
        profit_loss_long_short = []     # List of profits and losses by longs and shorts

        signal_series = pattern_signal_series_outside   # Default value if both Settings set to False

        if use_level_rejection:
            signal_series = rejection_signals_series_outside

        elif use_pattern_recognition:
            signal_series = pattern_signal_series_outside

        elif use_piercing_signal:
            signal_series = pierce_signals_series_outside

        if use_pattern_recognition or use_piercing_signal or use_level_rejection:
            for signal_index, signal_value in enumerate(signal_series):

                # LONG TRADES LOGIC
                if signal_value == 100 and longs_allowed:

                    trades_counter += 1
                    trade_direction.append('Long')
                    signal_candle_date = (filtered_df_original.iloc[signal_index]['Date']).strftime('%Y-%m-%d')
                    signal_candle_time = filtered_df_original.iloc[signal_index]['Time']
                    signal_candle_open = round(filtered_df_original.iloc[signal_index]['Open'], 3)
                    signal_candle_high = round(filtered_df_original.iloc[signal_index]['High'], 3)
                    signal_candle_low = round(filtered_df_original.iloc[signal_index]['Low'], 3)
                    signal_candle_close_entry = round(filtered_df_original.iloc[signal_index]['Close'], 3)   # ENTRY


                    stop_loss_price = None
                    take_profit_price = None
                    if stop_loss_as_candle_min_max:     # STOP as candle low
                        stop_loss_price = (signal_candle_low - stop_loss_offset)
                        take_profit_price = ((((signal_candle_close_entry - stop_loss_price) * risk_reward_simulation) +
                                              signal_candle_close_entry) + stop_loss_offset)

                    elif stop_loss_price_as_dollar_amount:  # STOP as distance from entry price
                        stop_loss_price = signal_candle_close_entry - rr_dollar_amount
                        take_profit_price = signal_candle_close_entry + (rr_dollar_amount * risk_reward_ratio)

                    elif stop_loss_as_plus_candle:
                        stop_loss_price = (signal_candle_low - ((signal_candle_close_entry - signal_candle_low)
                                                                * sl_offset_multiplier))
                        take_profit_price = (((signal_candle_close_entry - stop_loss_price) * risk_reward_simulation) +
                                             signal_candle_close_entry)
                    else:
                        print('Stop loss condition is not properly defined')

                    # take_profit_price = ((signal_candle_close_entry - signal_candle_low) * risk_reward
                    #                      + signal_candle_close_entry)
                    print('------------------------------------------------------------------------------------------')
                    print(f'▲ ▲ ▲ OPEN LONG TRADE: ▲ ▲ ▲ {signal_candle_date} {signal_candle_time}')
                    print(f'Entry price: {signal_candle_close_entry}')
                    print(f'Take: {round(take_profit_price, 3)} ({risk_reward_simulation}RR)')
                    print(f'Stop: {stop_loss_price}')
                    print()
                    print(f'Current (signal) candle OHLC | O {signal_candle_open}, H {signal_candle_high}, '
                          f'L {signal_candle_low}, C {signal_candle_close_entry}')
                    for j in range(signal_index + 1, len(filtered_df_original)):
                        current_candle_date = (filtered_df_original.iloc[j]['Date']).strftime('%Y-%m-%d')
                        current_candle_time = (filtered_df_original.iloc[j]['Time'])
                        current_candle_open = filtered_df_original.iloc[j]['Open']
                        current_candle_high = filtered_df_original.iloc[j]['High']
                        current_candle_low = filtered_df_original.iloc[j]['Low']
                        current_candle_close = filtered_df_original.iloc[j]['Close']

                        print('Next candle: ', current_candle_date, current_candle_time, '|',
                              'O', current_candle_open,
                              'H', current_candle_high,
                              'L', current_candle_low,
                              'C', current_candle_close)

                        if current_candle_open > stop_loss_price:

                            if current_candle_low <= stop_loss_price and current_candle_high >= take_profit_price:
                                trade_result_both.append(1)

                            elif current_candle_low <= stop_loss_price:
                                trade_result.append((stop_loss_price - spread) -
                                                    (signal_candle_close_entry + spread))
                                trade_result_longs.append((stop_loss_price - spread) -
                                                          (signal_candle_close_entry + spread))
                                profit_loss_long_short.append('LongLoss')
                                print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date} {current_candle_time}')
                                print()
                                print(f'Trade Close Price: {round(stop_loss_price, 3)}')
                                print(
                                  f'P/L: ${round((stop_loss_price - spread) - (signal_candle_close_entry + spread), 3)}'
                                )
                                print(
                                    '---------------------------------------------'
                                    '---------------------------------------------'
                                )
                                break

                            elif current_candle_high >= take_profit_price:
                                trade_result.append(take_profit_price - (signal_candle_close_entry + spread))
                                trade_result_longs.append(take_profit_price - (signal_candle_close_entry + spread))
                                profit_loss_long_short.append('LongProfit')
                                print(f'○ ○ ○ Take profit hit ○ ○ ○ at {current_candle_date} {current_candle_time}')
                                print()
                                print(f'Trade Trade Close Price: {round(take_profit_price, 3)}')
                                print(f'P/L: ${round(take_profit_price - (signal_candle_close_entry + spread), 3)}')
                                print(
                                    '---------------------------------------------'
                                    '---------------------------------------------'
                                )
                                break

                            else:
                                pass
                        else:       # IN CASE OF GAP DOWN, WHEN NEXT CANDLE OPENS LOWER THAN PREV. CANDLE STOP
                            trade_result.append((stop_loss_price - spread) - (signal_candle_close_entry + spread))
                            trade_result_longs.append((stop_loss_price - spread) - (signal_candle_close_entry + spread))
                            profit_loss_long_short.append('LongLoss')
                            print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date} {current_candle_time}')
                            print()
                            print(f'Trade Close Price: {round(stop_loss_price, 3)}')
                            print(
                                f'P/L: ${round((stop_loss_price - spread) - (signal_candle_close_entry + spread), 3)}'
                            )
                            print(
                                '---------------------------------------------'
                                '---------------------------------------------'
                            )
                            break

                # SHORT TRADES LOGIC
                elif signal_value == -100 and shorts_allowed:
                    trades_counter += 1
                    trade_direction.append('Short')
                    signal_candle_date = (filtered_df_original.iloc[signal_index]['Date']).strftime('%Y-%m-%d')
                    signal_candle_time = filtered_df_original.iloc[signal_index]['Time']
                    signal_candle_open = round(filtered_df_original.iloc[signal_index]['Open'], 3)
                    signal_candle_high = round(filtered_df_original.iloc[signal_index]['High'], 3)
                    signal_candle_low = round(filtered_df_original.iloc[signal_index]['Low'], 3)
                    signal_candle_close_entry = round(filtered_df_original.iloc[signal_index]['Close'], 3)


                    stop_loss_price = None
                    take_profit_price = None

                    if stop_loss_as_candle_min_max:
                        stop_loss_price = signal_candle_high + stop_loss_offset
                        take_profit_price = ((signal_candle_close_entry -
                                              ((stop_loss_price - signal_candle_close_entry)
                                               * risk_reward_simulation))) - stop_loss_offset

                    elif stop_loss_price_as_dollar_amount:  # STOP as distance from entry price
                        stop_loss_price = signal_candle_close_entry + rr_dollar_amount
                        take_profit_price = signal_candle_close_entry - (rr_dollar_amount * risk_reward_ratio)

                    elif stop_loss_as_plus_candle:
                        # Adding size of the signal candle to the stop
                        stop_loss_price = (signal_candle_high +
                                           ((signal_candle_high - signal_candle_close_entry)
                                            * sl_offset_multiplier))
                        take_profit_price = (signal_candle_close_entry -
                                             ((stop_loss_price - signal_candle_close_entry) * risk_reward_simulation))
                    else:
                        print('Stop loss condition is not properly defined')

                    print('------------------------------------------------------------------------------------------')
                    print(f'▼ ▼ ▼ OPEN SHORT TRADE: ▼ ▼ ▼ {signal_candle_date} {signal_candle_time}')
                    print(f'Entry price: {signal_candle_close_entry}')
                    print(f'Stop: {stop_loss_price}')
                    print(f'Take: {round(take_profit_price, 3)} ({risk_reward_simulation}RR)')
                    print()
                    print(f'Current (signal) candle OHLC | O {signal_candle_open}, H {signal_candle_high}, '
                          f'L {signal_candle_low}, C {signal_candle_close_entry}')
                    for j in range(signal_index + 1, len(filtered_df_original)):
                        current_candle_date = (filtered_df_original.iloc[j]['Date']).strftime('%Y-%m-%d')
                        current_candle_time = (filtered_df_original.iloc[j]['Time'])
                        current_candle_open = filtered_df_original.iloc[j]['Open']
                        current_candle_high = filtered_df_original.iloc[j]['High']
                        current_candle_low = filtered_df_original.iloc[j]['Low']
                        current_candle_close = filtered_df_original.iloc[j]['Close']

                        print('Next candle: ', current_candle_date, current_candle_time, '|',
                              'O', current_candle_open,
                              'H', current_candle_high,
                              'L', current_candle_low,
                              'C', current_candle_close)
                        if current_candle_open < stop_loss_price:
                            if current_candle_high >= stop_loss_price and current_candle_low <= take_profit_price:
                                trade_result_both.append(1)

                            elif current_candle_high >= stop_loss_price:
                                trade_result.append((signal_candle_close_entry - spread) - (stop_loss_price + spread))
                                trade_result_shorts.append((signal_candle_close_entry - spread) -
                                                           (stop_loss_price + spread))
                                profit_loss_long_short.append('ShortLoss')
                                print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date} {current_candle_time}')
                                print()
                                print(f'Trade Close Price: {round(stop_loss_price, 3)}')
                                print(
                                  f'P/L: ${round((signal_candle_close_entry - spread) - (stop_loss_price + spread), 3)}'
                                )
                                print(
                                    '---------------------------------------------'
                                    '---------------------------------------------'
                                )
                                break

                            elif current_candle_low <= take_profit_price:
                                trade_result.append((signal_candle_close_entry - spread) - take_profit_price)
                                trade_result_shorts.append((signal_candle_close_entry - spread) - take_profit_price)
                                profit_loss_long_short.append('ShortProfit')
                                print(f'○ ○ ○ Take profit hit ○ ○ ○ at {current_candle_date} {current_candle_time}')
                                print()
                                print(f'Trade Close Price: {round(take_profit_price, 3)}')
                                print(f'P/L: ${round((signal_candle_close_entry - spread) - take_profit_price, 3)}')
                                print(
                                    '---------------------------------------------'
                                    '---------------------------------------------'
                                )

                                break

                            else:
                                pass
                        else:   # IN CASE OF GAP UP, WHEN NEXT CANDLE OPENS HIGHER THAN PREV. CANDLE STOP
                            trade_result.append((signal_candle_close_entry - spread) - (stop_loss_price + spread))
                            trade_result_shorts.append((signal_candle_close_entry - spread) -
                                                       (stop_loss_price + spread))
                            profit_loss_long_short.append('ShortLoss')
                            print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date} {current_candle_time}')
                            print()
                            print(f'Trade Close Price: {round(stop_loss_price, 3)}')
                            print(
                                f'P/L: ${round((signal_candle_close_entry - spread) - (stop_loss_price + spread), 3)}'
                            )
                            print(
                                '---------------------------------------------'
                                '---------------------------------------------'
                            )
                            break

            return (trade_result_both, trade_result, trades_counter, trade_direction, profit_loss_long_short,
                    trade_result_longs, trade_result_shorts)
    else:
        print('Trade simulation is OFF')
        return None, None, None, None, None, None, None   # Return Nones in order to avoid error when function is OFF


(trade_result_both_to_trade_analysis, trade_results_to_trade_analysis, trades_counter_to_trade_analysis,
 trade_direction_to_trade_analysis, profit_loss_long_short_to_trade_analysis, trade_result_longs_to_trade_analysis,
 trade_result_shorts_to_trade_analysis) = trades_simulation(filtered_by_date_dataframe_original, risk_reward_ratio,
                                                            stop_loss_offset_multiplier)


def trades_analysis(trade_result_both, trade_result, trades_counter, trade_direction, profit_loss_long_short, 
                    trade_result_longs, trade_result_short, df_csv, df_api):

    if (show_trade_analysis and start_simulation and
            (use_piercing_signal or use_pattern_recognition or use_level_rejection)):

        if dataframe_source_api_or_csv:
            first_row = df_api.iloc[0]['Date']
            last_row = df_api.iloc[-1]['Date']
        else:
            first_row = df_csv.iloc[0]['Date']
            last_row = df_csv.iloc[-1]['Date']
        print()
        print('*****************************************************************************************')
        print('-------------------------------------TRADES ANALYSIS-------------------------------------')
        print('*****************************************************************************************')
        print(f'Ticker: {ticker_name}')
        print()
        print(f'Selected Date range: {start_date} - {end_date}'.upper(),
              f'(available period: {first_row}-{last_row})'.title()
              )
        print()

        if trades_counter == 0:
            print("No trades were placed! Try other pattern or broader date range")

        rounded_trades_list = 0
        try:
            rounded_trades_list = [round(num, 3) for num in trade_result]   # List of all trades in dollar amount
            # print(f"Trades List: {rounded_trades_list}")
        except TypeError:
            print(f'Trades List: {rounded_trades_list}')

        outcomes_string = []     # List of trade outcomes: profit or loss in order to calculate profitability %
        outcomes_positive = []      # List of positive trades

        outcomes_negative = []      # List of negative trades

        try:
            for num in rounded_trades_list:
                if num > 0:
                    outcomes_string.append('profit')
                    outcomes_positive.append(num)
                else:
                    outcomes_string.append('loss')
                    outcomes_negative.append(num)
            # print(f'Profitable trades list: {outcomes_positive}')
            # print(f'Losing trades list: {outcomes_negative}')
        except TypeError:
            print('Profitable trades list: No trades')
            print('Losing trades list: No trades')
        # Accumulate the sum of consecutive elements to illustrate balance change over time
        results_as_balance_change = []

        running_sum = 0
        try:
            running_sum = rounded_trades_list[0]
        except IndexError:
            pass

        for num in rounded_trades_list[1:]:
            running_sum += num
            results_as_balance_change.append(running_sum)

        rounded_results_as_balance_change = [round(x, 3) for x in results_as_balance_change]
        trades_count = len(outcomes_string)  # Total trades number
        profitable_trades_count = outcomes_string.count('profit')    # Profitable trades number
        loss_trades_count = outcomes_string.count('loss')    # Losing trades number

        win_percent = 0
        try:
            win_percent = (profitable_trades_count * 100) / trades_count    # Profitable trades %
        except ZeroDivisionError:
            pass

        loss_percent = 0
        try:
            loss_percent = (loss_trades_count * 100) / trades_count     # Losing trades %
        except ZeroDivisionError:
            pass
        candles_number_analyzed = len(filtered_by_date_dataframe)      # Total candles in analysis
        trades_per_candle = round(trades_count / candles_number_analyzed, 2)  # How many trades are placed in one day
        days_per_trade = 0
        try:
            days_per_trade = round(1 / trades_per_candle)      # 1 trade is placed in how many days
        except ZeroDivisionError:
            pass
        count_longs = trade_direction.count('Long')
        count_shorts = trade_direction.count('Short')
        try:
            count_profitable_longs_percent = round((profit_loss_long_short.count('LongProfit') * 100) /
                                                   count_longs, 2)
        except ZeroDivisionError:
            count_profitable_longs_percent = 0
            # print("No long trades were made")
        try:
            count_profitable_shorts_percent = round((profit_loss_long_short.count('ShortProfit') * 100) /
                                                    count_shorts, 2)
        except ZeroDivisionError:
            count_profitable_shorts_percent = 0
            # print("No short trades were made")

        # print(f'{profit_loss_long_short}')
        # print(f'List {trade_direction}')
        # print(f'Balance change over time list: {rounded_results_as_balance_change}')
        print()
        print(f'Spread: ${spread}')
        print(f'Total candles in range: {candles_number_analyzed}'.title())
        if days_per_trade > 0:
            print(f'Trades per candle: {trades_per_candle} or 1 trade every {days_per_trade} candles'.title())
        else:
            print('Trades per day: 0')
        print(f'Trades count: {trades_counter}'.title())
        print(f'Closed trades: {trades_count}'.title())
        print('**************************')
        print(f'*  risk_reward_ratio: {risk_reward_ratio}  *')
        print('**************************')
        print(f'Pattern: {active_pattern_list}')
        print()
        print(f'Both trades for long signals: {sum(trade_result_both)}')
        print(f'Profitable trades: {profitable_trades_count} ({round(win_percent, 2)}%)'.title())
        print(f'Losing trades: {loss_trades_count} ({round(loss_percent, 2)}%)'.title())
        print()
        print(f'Long trades: {count_longs} ({count_profitable_longs_percent}% profitable out of all longs) '
              f'P/L: ${round(sum(trade_result_longs), 2)}'.title())
        print(f'Short trades: {count_shorts} ({count_profitable_shorts_percent}% profitable out of all shorts) '
              f'P/L: ${round(sum(trade_result_short), 2)}'.title())
        print()

        try:
            print(f'Best trade: ${max(rounded_trades_list)}'.title())
        except ValueError:
            print('Best trade: $0')

        try:
            print(f'Worst trade: ${min(rounded_trades_list)}'.title())
        except ValueError:
            print('Worst trade: $0')

        print()

        if len(outcomes_positive) > 0:
            print(f'Average profitable trade: ${round(statistics.mean(outcomes_positive), 2)}')
        else:
            print(f'Average profitable trade: No profitable trades')

        if len(outcomes_negative) > 0:
            print(f'Average losing trade: ${round(statistics.mean(outcomes_negative), 2)}')
        else:
            print(f'Average losing trade: No losing trades')

        print()
        # Calculating mathematical expectation

        prob_per_trade = 1 / trades_count
        math_expectation = round(sum([outcome * prob_per_trade for outcome in trade_result]), 2)

        print(f'Expectation: ${math_expectation}')
        print()

        spread_loss = -1 * ((loss_trades_count * (spread * 2)) + (profitable_trades_count * spread))
        pending_order_spread_loss = -1 * (loss_trades_count * spread)

        print(f'Spread loss: ${spread_loss}'.title())
        print(f'If Pending Order spread loss : ${pending_order_spread_loss}'.title())
        print()

        p_n_l = round(sum(trade_result), 2)

        print(f'If not spread profit/loss: ${round(p_n_l - spread_loss, 2)}'.title())
        print(f'If pending order dollar per share profit/loss: ${p_n_l - pending_order_spread_loss}'.title())
        print('***************************************************************************************')
        print(f'*                       Dollar per Share profit/loss: ${p_n_l}                        *'.title())
        print('***************************************************************************************')

        return rounded_trades_list, rounded_results_as_balance_change

    else:
        print('Trade analysis is OFF')
        print()
        return None, None    # Return Nones in order to avoid error when function is OFF


rounded_trades_list_to_chart_profits_losses, rounded_results_as_balance_change_to_chart_profits = (
    trades_analysis(trade_result_both_to_trade_analysis, trade_results_to_trade_analysis,
                    trades_counter_to_trade_analysis, trade_direction_to_trade_analysis,
                    profit_loss_long_short_to_trade_analysis, trade_result_longs_to_trade_analysis,
                    trade_result_shorts_to_trade_analysis, dataframe_from_csv, dataframe_from_api))

#  ----------------------------------------------
#  PLOT CHART
#  ----------------------------------------------


def plot_line_chart(df):

    if show_line_chart:
        plt.figure(figsize=(10, 6))
        plt.plot(df['Datetime'], df['Close'], label='Ticker prices', marker='o')
        plt.title(f'{ticker_name}'.upper())
        plt.xlabel('Index')
        plt.ylabel('Price')
        plt.legend()


plot_line_chart(filtered_by_date_dataframe)


# BALANCE CHANGE CHART
def plot_line_chart_balance_change(rounded_results_as_balance_change):

    if show_balance_change_line_chart and start_simulation and show_trade_analysis:
        plt.figure(figsize=(10, 6))
        try:
            plt.plot(rounded_results_as_balance_change)
        except ValueError:
            print('No balance change chart to print (Trade analysis is OFF)\n')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title(f'Balance change over specified {start_date} - {end_date} date range ({ticker_name})')
        plt.grid(axis='y')


plot_line_chart_balance_change(rounded_results_as_balance_change_to_chart_profits)


# P/L LINE CHART
def plot_line_chart_profits_losses(rounded_trades_list):

    if show_profits_losses_line_chart and start_simulation:
        plt.figure(figsize=(10, 6))
        plt.plot(rounded_trades_list)
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('Trades over specified date range')
        plt.grid(axis='y')


plot_line_chart_profits_losses(rounded_trades_list_to_chart_profits_losses)


#  ----------------------------------------------
#  HIGHLIGHT SIGNALS
#  ----------------------------------------------


# date_time_dates = pd.to_datetime(filtered_by_date_dataframe['Datetime'])
# print('Date_time_dates: \n', date_time_dates)


def highlight_signal_on_line_chart(df):

    if show_signal_line_chart:
        for i, s in enumerate(pattern_signal_series_outside):
            if s == 100:
                signal_date = df['Datetime'].iloc[i].strftime("%d-%m-%Y-%H-%M")
                annotation_text = f'Bullish signal on {signal_date} in {file_path}'
                # the point where the arrow will be pointing to:
                plt.annotate(annotation_text,
                             xy=(df['Datetime'].iloc[i], df['Close'].iloc[i]),
                             xytext=(df['Datetime'].iloc[i], df['Close'].iloc[i] + 100),
                             arrowprops=dict(arrowstyle='->')
                             )
            elif s == -100:
                signal_date = df['Datetime'].iloc[i].strftime("%d-%m-%Y-%H-%M")
                annotation_text = f'Bearish signal on {signal_date} {file_path}'
                # the point where the arrow will be pointing to:
                plt.annotate(annotation_text,
                             xy=(df['Datetime'].iloc[i], df['Close'].iloc[i]),
                             xytext=(df['Datetime'].iloc[i], df['Close'].iloc[i] + 100),
                             arrowprops=dict(arrowstyle='->')
                             )


highlight_signal_on_line_chart(filtered_by_date_dataframe)


#  CANDLESTICK CHART
def plot_candlestick_chart(df, pattern_signals_series, pierce_signals_series,
                           sr_timeframe, level_discovery_signals_series, rejection_signals_series):

    if show_candlestick_chart:

        try:
            pattern_signals_series.reset_index(drop=True, inplace=True)

        except AttributeError:
            pass

        # df.set_index('Datetime', inplace=True)
        plots_list = []

        if show_level_rejection_signals:
            for i, s in enumerate(level_discovery_signals_series):
                if s != 'NaN':
                    plots_list.append(mpf.make_addplot(level_discovery_signals_series, type='scatter', color='black',
                                                       markersize=250, marker='*', panel=1))
            for i, s in enumerate(rejection_signals_series):
                if s != 'NaN':
                    plots_list.append(mpf.make_addplot(rejection_signals_series, type='scatter', color='black',
                                                       markersize=250, marker='+', panel=1))

        # Printing Swing Highs/Lows on chart
        if show_swing_highs_lows:
            swing_highs = talib.MAX(df['High'], sr_timeframe)
            swing_lows = talib.MIN(df['Low'], sr_timeframe)

            plots_list = [mpf.make_addplot(swing_highs, scatter=True, marker='v', markersize=50, color='green'),
                          mpf.make_addplot(swing_lows, scatter=True, marker='^', markersize=50, color='red')]
            # print('Print plots_list inside swing high: ', plots_list)
        else:
            print('Swing Highs/Lows showing is switched off')

        #  Converting zeros to NAN more suitable for plotting. Skip values which are true, others replace NaN
        pattern_signals_with_nan = None

        try:
            pattern_signals_with_nan = pattern_signals_series.where(pattern_signals_series != 0, np.nan)

        except AttributeError:
            pass

        # Iterate over signals and add non-zero signals to add_plots
        # Need to check it to avoid empty array error
        if use_pattern_recognition:
            if pattern_signals_with_nan is not None and not pattern_signals_with_nan.isna().all():
                for i, s in enumerate(pattern_signals_with_nan):
                    if s != 'NaN':
                        # Add signals as a subplot
                        plots_list.append(mpf.make_addplot(pattern_signals_with_nan,
                                                           type='scatter', color='black',
                                                           markersize=250, marker='+', panel=1))
        else:
            print('Patterns showing is switched off')
        # print('Print plots_list after patterns append: \n', plots_list)

        pierce_signals_with_nan = None

        try:
            pierce_signals_with_nan = pierce_signals_series.where(pierce_signals_series != 0, np.nan)
        except AttributeError:
            pass
        if use_piercing_signal:     # Need to check it to avoid empty array error
            if pierce_signals_with_nan is not None and not pierce_signals_with_nan.isna().all():
                for i, s in enumerate(pierce_signals_with_nan):
                    if s != 'NaN':
                        # Add signals as a subplot
                        plots_list.append(mpf.make_addplot(pierce_signals_with_nan,  # Add the signals as a subplot
                                                           type='scatter', color='blue',
                                                           markersize=250, marker='*', panel=1))

        else:
            print('Pierce showing is switched off')

        print()

        if use_find_levels:
            mpf.plot(df, type='candle', figsize=(12, 6),
                     alines=dict(alines=levels_points_for_chart, linewidths=2, alpha=0.4),
                     style='yahoo', title=f'{ticker_name}'.upper(), addplot=plots_list)
        else:
            mpf.plot(df, type='candle', figsize=(12, 6),
                     style='yahoo', title=f'{ticker_name}'.upper(), addplot=plots_list)


try:
    plot_candlestick_chart(filtered_by_date_dataframe,
                           pattern_signal_series_outside, pierce_signals_series_outside, sr_levels_timeframe,
                           level_discovery_signals_series_out, rejection_signals_series_outside)

except KeyboardInterrupt:
    print('Program stopped manually')
