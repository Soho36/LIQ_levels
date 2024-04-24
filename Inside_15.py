import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import statistics
from API_or_Json import dataframe_from_api


# ------------------------------------------
# The list of paths to datafiles:

file_path = 'History_data/MT5/TSLA_M15.csv'
# ------------------------------------------
# pd.set_option('display.max_columns', 10)  # Uncomment to display all columns

# **************************************** SETTINGS **************************************
# symbol = 'TSLA'
dataframe_source_api_or_csv = False    # True for API or response file, False for CSV
start_date = '2024-01-09'       # Choose the start date to begin from
end_date = '2024-01-09'         # Choose the end date

# SIMULATION AND ANALYSIS
start_simulation = True

# ENTRY CONDITIONS
use_candle_high_or_low_as_entry = True
use_candle_close_as_entry = False
longs_allowed = True            # Allow or disallow trade direction
shorts_allowed = True          # Allow or disallow trade direction
inside_bar_ratio = 3

# RISK MANAGEMENT
spread = 0
risk_reward_ratio = 1                # Chose risk/reward ratio
stop_loss_as_candle_high_low = True
stop_loss_offset = 0                 # Is added to SL for Shorts and subtracted for Longs ($ amount)

# CHARTS
show_candlestick_chart = True
show_balance_change_line_chart = False   # Only when Simulation is True

# INDICATORS
show_vwap = True
show_inside_bar_signals = True
find_price_levels = True

# ******************************************************************************


def getting_dataframe_from_file(path):

    print()

    columns_to_parse = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Filename']

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
        print('NB! Dataframe is empty, check the date range!')
        exit()

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


if find_price_levels:
    def levels_discovery(filtered_df):
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
     sr_levels_out) = levels_discovery(filtered_by_date_dataframe)

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
# print('SR_levels_out: \n', sr_levels_out)
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


def fill_column_with_first_non_null_value(df, column_idx):  # Price levels startpoints logic

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
# print('Dataframe level columns: \n', filtered_by_date_dataframe)

# *******************************************************************************************************************


def vwap_calculation(df):
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3

    cumulative_tp_volume = typical_price * df['Volume']

    cumulative_volume = df['Volume']

    vwap = cumulative_tp_volume.cumsum() / cumulative_volume.cumsum()
    return vwap


vw_points_series_outside = vwap_calculation(filtered_by_date_dataframe_original)
print()
# print('VWap points: ', vw_points_series_outside)


#  ----------------------------------------------
#  INSIDE BAR SEARCHING
#  ----------------------------------------------

#  L1 <= L AND H <= H1 AND H-L < H1-L1

def inside_bar_recognition(df):
    all_inside_bar_signals = []     # All inside bar signals
    small_inside_bar_signals = []   # Signals of inside bars smaller than predefined number

    df.reset_index(inplace=True)
    print()
    # print('inside bar DF: \n', df)

    first_candle_size = df.iloc[0]['High'] - df.iloc[0]['Low']  # The size of the day opening candle
    for index, row in df.iterrows():
        current_candle_low = row['Low']
        current_candle_high = row['High']
        previous_candle_low = df.iloc[index - 1]['Low']
        previous_candle_high = df.iloc[index - 1]['High']

        if (previous_candle_low <= current_candle_low and
                current_candle_high <= previous_candle_high and
                (current_candle_high - current_candle_low) < (previous_candle_high - previous_candle_low)):
            all_inside_bar_signals.append(100)

            if first_candle_size / (current_candle_high - current_candle_low) >= inside_bar_ratio:
                small_inside_bar_signals.append(100)
            else:
                small_inside_bar_signals.append(None)
        else:
            all_inside_bar_signals.append(None)
            small_inside_bar_signals.append(None)

    print()
    print('First_candle_size: ', first_candle_size)
    print()
    print('Inside bar signals: ', all_inside_bar_signals)
    print()
    print('Small inside bar signals: ', small_inside_bar_signals)
    inside_bar_signals_series = pd.Series(all_inside_bar_signals)
    small_inside_bar_signals_series = pd.Series(small_inside_bar_signals)
    return inside_bar_signals_series, small_inside_bar_signals_series


inside_bar_signals_series_outside, small_inside_bar_signals_series_outside = (
    inside_bar_recognition(filtered_by_date_dataframe)
)

#  ----------------------------------------------
#  TRADES SIMULATION
#  ----------------------------------------------


def trades_simulation(filtered_df_original, risk_reward_simulation):
    # print('!!!!', filtered_df_original)
    if start_simulation:
        trades_counter = 0
        trade_result_both = []
        trade_result = []
        trade_result_longs = []
        trade_result_shorts = []
        trade_direction = []
        profit_loss_long_short = []     # List of profits and losses by longs and shorts

        def trades_logic(signal, counter):
            # LONG TRADES LOGIC
            if signal == 100 and longs_allowed:

                # signal_candle_date = (filtered_df_original.iloc[signal_index]['Date']).strftime('%Y-%m-%d')
                # signal_candle_time = filtered_df_original.iloc[signal_index]['Time']
                signal_candle_low = round(filtered_df_original.iloc[signal_index]['Low'], 3)
                entry_price = None

                if use_candle_close_as_entry:
                    entry_price = round(filtered_df_original.iloc[signal_index]['Close'], 3)   # ENTRY

                elif use_candle_high_or_low_as_entry:
                    entry_price = round(filtered_df_original.iloc[signal_index]['High'], 3)

                else:
                    print("Choose entry type".upper())

                stop_loss_price = None
                take_profit_price = None

                if stop_loss_as_candle_high_low:  # STOP as candle low
                    stop_loss_price = (signal_candle_low - stop_loss_offset)
                    take_profit_price = (
                            (((entry_price - stop_loss_price) * risk_reward_simulation)
                             + entry_price) + stop_loss_offset
                    )
                else:
                    print('Stop loss condition is not properly defined')

                trade_is_open = False

                for j in range(signal_index + 1, len(filtered_df_original)):
                    current_candle_date = (filtered_df_original.iloc[j]['Date']).strftime('%Y-%m-%d')
                    current_candle_time = (filtered_df_original.iloc[j]['Time'])
                    # current_candle_open = filtered_df_original.iloc[j]['Open']
                    current_candle_high = filtered_df_original.iloc[j]['High']
                    current_candle_low = filtered_df_original.iloc[j]['Low']
                    # current_candle_close = filtered_df_original.iloc[j]['Close']

                    if current_candle_high >= entry_price and trade_is_open is False:
                        print(
                            '------------------------------------------------------------------------------------------'
                        )
                        print(f'▲ ▲ ▲ OPEN LONG TRADE: ▲ ▲ ▲ {current_candle_date} {current_candle_time}')
                        print(f'Entry price: {entry_price}')
                        print(f'Take: {round(take_profit_price, 3)} ({risk_reward_simulation}RR)')
                        print(f'Stop: {stop_loss_price}')
                        print()
                        counter += 1
                        trade_direction.append('Long')

                        trade_is_open = True

                    if trade_is_open:
                        if current_candle_low <= stop_loss_price:
                            trade_result.append((stop_loss_price - spread) -
                                                (entry_price + spread))
                            trade_result_longs.append((stop_loss_price - spread) -
                                                      (entry_price + spread))
                            profit_loss_long_short.append('LongLoss')
                            print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date} {current_candle_time}')
                            print()
                            print(f'Trade Close Price: {round(stop_loss_price, 3)}')
                            print(
                              f'P/L: ${round((stop_loss_price - spread) - (entry_price + spread), 3)}'
                            )
                            print(
                                '---------------------------------------------'
                                '---------------------------------------------'
                            )
                            trade_is_open = False
                            break

                        elif current_candle_high >= take_profit_price:
                            trade_result.append(take_profit_price - (entry_price + spread))
                            trade_result_longs.append(take_profit_price - (entry_price + spread))
                            profit_loss_long_short.append('LongProfit')
                            print(f'○ ○ ○ Take profit hit ○ ○ ○ at {current_candle_date} {current_candle_time}')
                            print()
                            print(f'Trade Trade Close Price: {round(take_profit_price, 3)}')
                            print(f'P/L: ${round(take_profit_price - (entry_price + spread), 3)}')
                            print(
                                '---------------------------------------------'
                                '---------------------------------------------'
                            )
                            trade_is_open = False
                            break

                    else:
                        trade_is_open = False

                if trade_is_open:   # If trade is still opened in the end of the day - close at market
                    print('Close at market in the end of the day')

                else:
                    pass
                    # print('No trades STILL opened')

            # SHORT TRADES LOGIC
            if signal == -100 and shorts_allowed:

                # signal_candle_date = (filtered_df_original.iloc[signal_index]['Date']).strftime('%Y-%m-%d')
                # signal_candle_time = filtered_df_original.iloc[signal_index]['Time']
                signal_candle_high = round(filtered_df_original.iloc[signal_index]['High'], 3)
                entry_price = None

                if use_candle_close_as_entry:
                    entry_price = round(filtered_df_original.iloc[signal_index]['Close'], 3)  # ENTRY

                elif use_candle_high_or_low_as_entry:
                    entry_price = round(filtered_df_original.iloc[signal_index]['Low'], 3)

                else:
                    print("Choose entry type".upper())

                stop_loss_price = None
                take_profit_price = None

                if stop_loss_as_candle_high_low:  # STOP as candle low
                    stop_loss_price = signal_candle_high + stop_loss_offset
                    take_profit_price = ((entry_price -
                                          ((stop_loss_price - entry_price)
                                           * risk_reward_simulation))) - stop_loss_offset
                else:
                    print('Stop loss condition is not properly defined')

                trade_is_open = False

                for j in range(signal_index + 1, len(filtered_df_original)):
                    current_candle_date = (filtered_df_original.iloc[j]['Date']).strftime('%Y-%m-%d')
                    current_candle_time = (filtered_df_original.iloc[j]['Time'])
                    # current_candle_open = filtered_df_original.iloc[j]['Open']
                    current_candle_high = filtered_df_original.iloc[j]['High']
                    current_candle_low = filtered_df_original.iloc[j]['Low']
                    # current_candle_close = filtered_df_original.iloc[j]['Close']

                    if current_candle_low <= entry_price and trade_is_open is False:
                        print(
                            '------------------------------------------------------------------------------------------'
                        )
                        print(f'▼ ▼ ▼ OPEN SHORT TRADE: ▼ ▼ ▼ {current_candle_date} {current_candle_time}')
                        print(f'Entry price: {entry_price}')
                        print(f'Take: {round(take_profit_price, 3)} ({risk_reward_simulation}RR)')
                        print(f'Stop: {stop_loss_price}')
                        print()
                        counter += 1
                        trade_direction.append('Short')

                        trade_is_open = True

                    if trade_is_open:
                        if current_candle_high >= stop_loss_price:
                            trade_result.append((entry_price - spread) -
                                                (stop_loss_price + spread))
                            trade_result_shorts.append((entry_price - spread) -
                                                       (stop_loss_price + spread))
                            profit_loss_long_short.append('ShortLoss')
                            print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date} {current_candle_time}')
                            print()
                            print(f'Trade Close Price: {round(stop_loss_price, 3)}')
                            print(
                                f'P/L: ${round((entry_price - spread) - (stop_loss_price + spread), 3)}'
                            )
                            print(
                                '---------------------------------------------'
                                '---------------------------------------------'
                            )
                            trade_is_open = False
                            break

                        elif current_candle_low <= take_profit_price:
                            trade_result.append((entry_price - spread) - take_profit_price)
                            trade_result_shorts.append((entry_price - spread) - take_profit_price)
                            profit_loss_long_short.append('ShortProfit')
                            print(f'○ ○ ○ Take profit hit ○ ○ ○ at {current_candle_date} {current_candle_time}')
                            print()
                            print(f'Trade Close Price: {round(take_profit_price, 3)}')
                            print(f'P/L: ${round((entry_price - spread) - take_profit_price, 3)}')
                            print(
                                '---------------------------------------------'
                                '---------------------------------------------'
                            )
                            trade_is_open = False
                            break

                    else:
                        trade_is_open = False

                if trade_is_open:  # If trade is still opened in the end of the day - close at market
                    print('Close at market in the end of the day')

                else:
                    pass
                    # print('No trades STILL opened')

        signal_series = small_inside_bar_signals_series_outside

        for signal_index, signal_value, in enumerate(signal_series):

            trades_logic(signal_value, trades_counter)

        return (trade_result_both, trade_result, trades_counter, trade_direction, profit_loss_long_short,
                trade_result_longs, trade_result_shorts)
    else:
        print('Trade simulation is OFF')
        return None, None, None, None, None, None, None   # Return Nones in order to avoid error when function is OFF


(trade_result_both_to_trade_analysis, trade_results_to_trade_analysis, trades_counter_to_trade_analysis,
 trade_direction_to_trade_analysis, profit_loss_long_short_to_trade_analysis, trade_result_longs_to_trade_analysis,
 trade_result_shorts_to_trade_analysis) = trades_simulation(filtered_by_date_dataframe_original, risk_reward_ratio)


def trades_analysis(trade_result_both, trade_result, trades_counter, trade_direction, profit_loss_long_short, 
                    trade_result_longs, trade_result_short, df_csv, df_api):

    if start_simulation:

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
            print("No trades were placed!")

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
        print()
        print(f'Both trades: {sum(trade_result_both)}')
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
        try:
            prob_per_trade = 1 / trades_count
        except ZeroDivisionError:
            prob_per_trade = 0

        math_expectation = round(sum([outcome * prob_per_trade for outcome in trade_result]), 2)
        if prob_per_trade > 0:
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


# BALANCE CHANGE CHART
def plot_line_chart_balance_change(rounded_results_as_balance_change):

    if show_balance_change_line_chart and start_simulation:
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


#  ----------------------------------------------
#  HIGHLIGHT SIGNALS
#  ----------------------------------------------


#  CANDLESTICK CHART
def plot_candlestick_chart(df, vwap_series, inside_bar_series, small_inside_bar_series):

    df.set_index('Datetime', inplace=True)
    if show_candlestick_chart:

        plots_list = []

        if show_inside_bar_signals:
            for i, s in enumerate(inside_bar_series):
                if s != 'NaN':
                    plots_list.append(mpf.make_addplot(inside_bar_series, type='scatter', color='black',
                                                       markersize=250, marker='+', panel=1))
            for i, s in enumerate(small_inside_bar_series):
                if s != 'NaN':
                    plots_list.append(mpf.make_addplot(small_inside_bar_series, type='scatter', color='black',
                                                       markersize=250, marker='*', panel=1))

        else:
            print('Swing Highs/Lows showing is switched off')

        print()
        if show_vwap:
            plots_list.append(mpf.make_addplot(vwap_series, type='line', linewidths=0.2, alpha=0.7, color='yellow'))

        if find_price_levels:
            mpf.plot(df, type='candle', figsize=(12, 6),
                     alines=dict(alines=levels_points_for_chart, linewidths=2, alpha=0.4),
                     style='yahoo', title=f'{ticker_name}'.upper(), addplot=plots_list)

        else:
            mpf.plot(df, type='candle', figsize=(12, 6),
                     style='yahoo', title=f'{ticker_name}'.upper(), addplot=plots_list)


try:
    plot_candlestick_chart(filtered_by_date_dataframe, vw_points_series_outside,
                           inside_bar_signals_series_outside, small_inside_bar_signals_series_outside)

except KeyboardInterrupt:
    print('Program stopped manually')
