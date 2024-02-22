import talib
import pandas as pd
import os
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import statistics
from API_file import dataframe_from_api

# ------------------------------------------
# The list of paths to datafiles:
# file_path = 'TXT/merged_data.csv'
# file_path = 'TXT/exel.csv'
# file_path = 'TXT/spr.csv'
# file_path = 'TXT/zim.csv'
# file_path = 'TXT/extr.csv'
# file_path = 'TXT/aehr.csv'
file_path = 'TXT/tsla_D1.csv'
# file_path = 'TXT/neog_D1.csv'
# file_path = 'TXT/meta_D1.csv'
# file_path = 'TXT/tsla_m5.csv'
# file_path = 'TXT/tsla_m1.csv'
# file_path = 'TXT/MT4/BTCUSD_D1.csv'
# file_path = 'TXT/MT4/BTCUSD_m60.csv'
# file_path = 'TXT/MT4/BTCUSD_m5.csv'
# ------------------------------------------
# pd.set_option('display.max_columns', 10)  # Uncomment to display all columns


# ******************************************************************************
dataframe_source_api_or_csv = False    # True for API or response file, False for CSV
start_date = '2018-02-20'     # Choose the start date to begin from
end_date = '2024-02-05'     # Choose the end date
code_of_pattern = 50     # Choose the index of pattern (from Ta-lib patterns.csv)
risk_reward_ratio = 5   # Chose risk/reward ratio (how much you are aiming to win compared to lose)
stop_loss_as_candle_min_max = True  # Must be True if next condition is false

stop_loss_as_plus_candle = False     # Must be True if previous condition is false
stop_loss_offset_multiplier = 1    # 1 places stop one candle away from H/L (only when stop_loss_as_plus_candle = True
# ******************************************************************************


def getting_dataframe_from_file(path):

    directory_path = 'TXT/'
    print()
    print('Datafiles in folder: ')
    for filename in os.listdir(directory_path):     # Making a list of files located in TXT folder
        print(filename)
    print()
    print(f'Current file is: {path}')

    columns_to_parce = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Filename']

    #  for MT4 files set dayfirst=False
    csv_df = pd.read_csv(path, parse_dates=[0], dayfirst=False, usecols=columns_to_parce)
    print()
    print(f'Dataframe derived from CSV:\n {csv_df}')
    print()
    return csv_df


dataframe_from_csv = getting_dataframe_from_file(file_path)


def date_range_func(df_csv, df_api, start, end):

    date_range = pd.date_range(start=start, end=end, freq='D')
    # print('Date range: \n', list(date_range))

    if dataframe_source_api_or_csv:
        df = df_api
        print(f'Dataframe derived from API:\n {df}', )
    else:
        df = df_csv

    date_column = df['Date']        # Select the 'Date' column from the DataFrame
    dates_in_range = date_column.isin(date_range)   # checks which dates from date_column fall within the generated
    # date range, resulting in a boolean mask
    df_filtered_by_date = df[dates_in_range]
    if df_filtered_by_date.empty:
        # print('NB! Dataframe is empty, check the date range!')
        raise ValueError('NB! Dataframe is empty, check the date range!')
    else:
        return df_filtered_by_date


filtered_by_date_dataframe = date_range_func(dataframe_from_csv, dataframe_from_api, start_date, end_date)

print()
print(f'Dataframe filtered by date:\n {filtered_by_date_dataframe}')
print()
print('************************************TRADES SIMULATION************************************')

#  ----------------------------------------------
#  PATTERN RECOGNITION
#  ----------------------------------------------

patterns_dataframe = pd.read_csv('Ta-lib patterns.csv')


def pattern_recognition_func(patterns_df, code):  # Reading Pattern codes from CSV

    pattern_code = patterns_df['PatternCode'].iloc[code]
    pattern_name = patterns_df['PatternName'].iloc[code]
    pattern_index = patterns_df.index[code]
    print()
    print(f'Current Pattern is: {pattern_code}, {pattern_name}, {pattern_index}')

    pattern_function = getattr(talib, pattern_code)
    signal = pattern_function(filtered_by_date_dataframe['Open'], filtered_by_date_dataframe['High'],
                              filtered_by_date_dataframe['Low'], filtered_by_date_dataframe['Close'])

    return signal


recognized_pattern = pattern_recognition_func(patterns_dataframe, code_of_pattern)  # Returns series
# print(recognized_pattern)


#  ----------------------------------------------
#  TRADES SIMULATION
#  ----------------------------------------------

# # STOP LOSS PRICE CALCULATION
# def stop_loss_price_definition(signal_candle_high_low_stop, filtered_df):
#     signal_candle_low = round(filtered_df.iloc[signal_index]['Low'], 2)
#     if signal_candle_high_low_stop:
#         stop_loss_price = signal_candle_low - sl_offset
#
#
# stop_loss_price_definition(use_signal_candle_high_low_as_stop)


def trades_simulation(filtered_df, risk_reward, sl_offset_multiplier):
    on_off = True
    if on_off:
        trades_counter = 0
        trade_result = []
        trade_result_longs = []
        trade_result_shorts = []
        trade_direction = []
        profit_loss_long_short = []     # List of profits and losses by longs and shorts
        for signal_index, signal_value in enumerate(recognized_pattern):

            # LONG TRADES LOGIC
            if signal_value == 100:
                trades_counter += 1
                trade_direction.append('Long')
                signal_candle_date = filtered_df.iloc[signal_index]['Date']
                signal_candle_open = round(filtered_df.iloc[signal_index]['Open'], 3)
                signal_candle_high = round(filtered_df.iloc[signal_index]['High'], 3)
                signal_candle_low = round(filtered_df.iloc[signal_index]['Low'], 3)
                signal_candle_close_entry = round(filtered_df.iloc[signal_index]['Close'], 3)

                stop_loss_price = None
                take_profit_price = None
                if stop_loss_as_candle_min_max:
                    stop_loss_price = signal_candle_low
                    take_profit_price = (((signal_candle_close_entry - signal_candle_low) * risk_reward) +
                                         signal_candle_close_entry)

                elif stop_loss_as_plus_candle:
                    stop_loss_price = (signal_candle_low - ((signal_candle_close_entry - signal_candle_low)
                                                            * sl_offset_multiplier))
                    take_profit_price = (((signal_candle_close_entry - stop_loss_price) * risk_reward) +
                                         signal_candle_close_entry)
                else:
                    print('Stop loss condition is not properly defined')

                # take_profit_price = ((signal_candle_close_entry - signal_candle_low) * risk_reward
                #                      + signal_candle_close_entry)
                print('------------------------------------------------------------------------------------------')
                print(f'▲ ▲ ▲ OPEN LONG TRADE: ▲ ▲ ▲ {signal_candle_date}')
                print(f'Entry price: {signal_candle_close_entry}')
                print(f'Take: {round(take_profit_price, 3)} ({risk_reward}RR)')
                print(f'Stop: {stop_loss_price}')
                print()
                print(f'Current (signal) candle OHLC | O {signal_candle_open}, H {signal_candle_high}, '
                      f'L {signal_candle_low}, C {signal_candle_close_entry}')
                for j in range(signal_index + 1, len(filtered_df)):
                    current_candle_date = filtered_df.iloc[j]['Date']
                    current_candle_open = filtered_df.iloc[j]['Open']
                    current_candle_high = filtered_df.iloc[j]['High']
                    current_candle_low = filtered_df.iloc[j]['Low']
                    current_candle_close = filtered_df.iloc[j]['Close']

                    print('Next candle: ', current_candle_date, '|',
                          'O', current_candle_open,
                          'H', current_candle_high,
                          'L', current_candle_low,
                          'C', current_candle_close)

                    if current_candle_high >= take_profit_price:
                        trade_result.append(take_profit_price - signal_candle_close_entry)
                        trade_result_longs.append(take_profit_price - signal_candle_close_entry)
                        profit_loss_long_short.append('LongProfit')
                        print(f'○ ○ ○ Take profit hit ○ ○ ○ at {current_candle_date}')
                        print()
                        print(f'Close price: {round(take_profit_price, 3)}')
                        print(f'P/L: ${round(take_profit_price - signal_candle_close_entry, 3)}')
                        print(
                            '------------------------------------------------------------------------------------------'
                        )
                        break
                    elif current_candle_low <= stop_loss_price:
                        trade_result.append(stop_loss_price - signal_candle_close_entry)
                        trade_result_longs.append(stop_loss_price - signal_candle_close_entry)
                        profit_loss_long_short.append('LongLoss')
                        print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date}')
                        print()
                        print(f'Close price: {round(stop_loss_price, 3)}')
                        print(f'P/L: ${round(stop_loss_price - signal_candle_close_entry, 3)}')
                        print(
                            '------------------------------------------------------------------------------------------'
                        )
                        break
                    else:
                        pass
                        # print('Still Open')

            # SHORT TRADES LOGIC
            elif signal_value == -100:
                trades_counter += 1
                trade_direction.append('Short')
                signal_candle_date = filtered_df.iloc[signal_index]['Date']
                signal_candle_open = round(filtered_df.iloc[signal_index]['Open'], 3)
                signal_candle_high = round(filtered_df.iloc[signal_index]['High'], 3)
                signal_candle_low = round(filtered_df.iloc[signal_index]['Low'], 3)
                signal_candle_close_entry = round(filtered_df.iloc[signal_index]['Close'], 3)

                stop_loss_price = None
                take_profit_price = None
                if stop_loss_as_candle_min_max:
                    stop_loss_price = signal_candle_high
                    take_profit_price = (signal_candle_close_entry -
                                         ((signal_candle_high - signal_candle_close_entry) * risk_reward))

                elif stop_loss_as_plus_candle:
                    # Basically adding size of the signal candle to the stop
                    stop_loss_price = (signal_candle_high +
                                       ((signal_candle_high - signal_candle_close_entry) * sl_offset_multiplier))
                    take_profit_price = (signal_candle_close_entry -
                                         ((stop_loss_price - signal_candle_close_entry) * risk_reward))
                else:
                    print('Stop loss condition is not properly defined')

                print('------------------------------------------------------------------------------------------')
                print(f'▼ ▼ ▼ OPEN SHORT TRADE: ▼ ▼ ▼ {signal_candle_date}')
                print(f'Entry price: {signal_candle_close_entry}')
                print(f'Stop: {stop_loss_price}')
                print(f'Take: {round(take_profit_price, 3)} ({risk_reward}RR)')
                print()
                print(f'Current (signal) candle OHLC | O {signal_candle_open}, H {signal_candle_high}, '
                      f'L {signal_candle_low}, C {signal_candle_close_entry}')
                for j in range(signal_index + 1, len(filtered_df)):
                    current_candle_date = filtered_df.iloc[j]['Date']
                    current_candle_open = filtered_df.iloc[j]['Open']
                    current_candle_high = filtered_df.iloc[j]['High']
                    current_candle_low = filtered_df.iloc[j]['Low']
                    current_candle_close = filtered_df.iloc[j]['Close']

                    print('Next candle: ', current_candle_date, '|',
                          'O', current_candle_open,
                          'H', current_candle_high,
                          'L', current_candle_low,
                          'C', current_candle_close)
                    if current_candle_low <= take_profit_price:
                        trade_result.append(signal_candle_close_entry - take_profit_price)
                        trade_result_shorts.append(signal_candle_close_entry - take_profit_price)
                        profit_loss_long_short.append('ShortProfit')
                        print(f'○ ○ ○ Take profit hit ○ ○ ○ at {current_candle_date}')
                        print()
                        print(f'Close price: {round(take_profit_price, 3)}')
                        print(f'P/L: ${round(signal_candle_close_entry - take_profit_price, 3)}')
                        print(
                            '------------------------------------------------------------------------------------------'
                        )

                        break
                    elif current_candle_high >= stop_loss_price:
                        trade_result.append(signal_candle_close_entry - stop_loss_price)
                        trade_result_shorts.append(signal_candle_close_entry - stop_loss_price)
                        profit_loss_long_short.append('ShortLoss')
                        print(f'□ □ □ Stop Loss hit □ □ □ at {current_candle_date}')
                        print()
                        print(f'Close price: {round(stop_loss_price, 3)}')
                        print(f'P/L: ${round(signal_candle_close_entry - stop_loss_price, 3)}')
                        print(
                            '------------------------------------------------------------------------------------------'
                        )
                        break
                    else:
                        pass

        return (trade_result, trades_counter, trade_direction, profit_loss_long_short, trade_result_longs,
                trade_result_shorts)


(trade_results_to_trade_analysis, trades_counter_to_trade_analysis, trade_direction_to_trade_analysis,
 profit_loss_long_short_to_trade_analysis, trade_result_longs_to_trade_analysis, trade_result_shorts_to_trade_analysis)\
    = trades_simulation(filtered_by_date_dataframe, risk_reward_ratio, stop_loss_offset_multiplier)


def trades_analysis(trade_result, trades_counter, trade_direction, profit_loss_long_short, df, trade_result_longs,
                    trade_result_short):

    on_off = True

    if on_off:

        first_row = df.iloc[0]['Date']
        last_row = df.iloc[-1]['Date']
        print()
        print('************************************TRADES ANALYSIS************************************')
        print()
        print(f'Selected Date range: {start_date} - {end_date}'.upper(),
              f'(available period: {first_row}-{last_row})'.title()
              )
        print()

        if trades_counter == 0:
            print("No trades were placed! Try other pattern or broader date range")

        rounded_trades_list = [round(num, 3) for num in trade_result]   # List of all trades results in dollar amount
        print(f"Trades List: {rounded_trades_list}")

        outcomes_string = []     # List of trade outcomes: profit or loss in order to calculate profitability %
        outcomes_positive = []      # List of positive trades
        outcomes_negative = []     # List of negative trades

        for num in rounded_trades_list:
            if num > 0:
                outcomes_string.append('profit')
                outcomes_positive.append(num)
            else:
                outcomes_string.append('loss')
                outcomes_negative.append(num)

        # Accumulate the sum of consecutive elements to illustrate balance change over time
        results_as_balance_change = []
        running_sum = rounded_trades_list[0]
        for num in rounded_trades_list[1:]:
            running_sum += num
            results_as_balance_change.append(running_sum)

        rounded_results_as_balance_change = [round(x, 3) for x in results_as_balance_change]

        # print(result)
        trades_count = len(outcomes_string)  # Total trades number
        profitable_trades_count = outcomes_string.count('profit')    # Profitable trades number
        loss_trades_count = outcomes_string.count('loss')    # Losing trades number
        win_percent = (profitable_trades_count * 100) / trades_count    # Profitable trades %
        loss_percent = (loss_trades_count * 100) / trades_count     # Losing trades %
        days_number_analyzed = len(filtered_by_date_dataframe)      # Total days(candles) in analysis
        trades_per_day = round(trades_count / days_number_analyzed, 2)  # How many trades are placed in one day
        days_per_trade = round(1 / trades_per_day)      # 1 trade is placed in how many days
        count_longs = trade_direction.count('Long')
        count_shorts = trade_direction.count('Short')
        count_profitable_longs_percent = round((profit_loss_long_short.count('LongProfit') * 100) / count_longs, 2)
        count_profitable_shorts_percent = round((profit_loss_long_short.count('ShortProfit') * 100) / count_shorts, 2)
        # print(f'{profit_loss_long_short}')
        # print(f'List {trade_direction}')
        print(f'Balance change over time list: {rounded_results_as_balance_change}')
        print(f'Total days in range: {days_number_analyzed}'.title())
        print(f'Trades per day: {trades_per_day} or 1 trade every {days_per_trade} days'.title())
        print(f'Trades count: {trades_counter}'.title())
        print(f'Closed trades: {trades_count}'.title())
        print()
        print(f'Profitable trades: {profitable_trades_count} ({round(win_percent, 2)}%)'.title())
        print(f'Losing trades: {loss_trades_count} ({round(loss_percent, 2)}%)'.title())
        print()
        print(f'Long trades: {count_longs} ({count_profitable_longs_percent}% profitable out of all longs) '
              f'P/L: ${round(sum(trade_result_longs), 2)}'.title())
        print(f'Short trades: {count_shorts} ({count_profitable_shorts_percent}% profitable out of all shorts) '
              f'P/L: ${round(sum(trade_result_short), 2)}'.title())
        print()
        print(f'Best trade: ${max(rounded_trades_list)}'.title())
        print(f'Worst trade: ${min(rounded_trades_list)}'.title())
        print()
        print(f'Average profitable trade: ${round(statistics.mean(outcomes_positive), 2)}')
        print(f'Average losing trade: ${round(statistics.mean(outcomes_negative), 2)}')
        print()
        print(f'Dollar per Share profit/loss: ${round(sum(trade_result), 2)}'.title())

        print('***************************************************************************************')

        return rounded_trades_list, rounded_results_as_balance_change


rounded_trades_list_to_chart_profits_losses, rounded_results_as_balance_change_to_chart_profits = trades_analysis(
    trade_results_to_trade_analysis, trades_counter_to_trade_analysis,
    trade_direction_to_trade_analysis, profit_loss_long_short_to_trade_analysis, dataframe_from_csv,
    trade_result_longs_to_trade_analysis, trade_result_shorts_to_trade_analysis)

#  ----------------------------------------------
#  PLOT CHART
#  ----------------------------------------------

#  Adding datetime column to dataframe for chart plotting
filtered_by_date_dataframe = (filtered_by_date_dataframe.assign(
    Datetime=(filtered_by_date_dataframe['Date'] + pd.to_timedelta(filtered_by_date_dataframe['Time']))))


def plot_line_chart(df):
    on_off = False   # To disable Line chart set to False

    if on_off:
        plt.figure(figsize=(15, 8))
        plt.plot(df['Datetime'], df['Close'], label='Ticker prices', marker='o')
        plt.title(f'{file_path}'.upper())
        plt.xlabel('Index')
        plt.ylabel('Price')
        plt.legend()


plot_line_chart(filtered_by_date_dataframe)


# BALANCE CHANGE CHART
def plot_line_chart_balance_change(rounded_results_as_balance_change):

    on_off = True

    if on_off:
        plt.figure(figsize=(15, 8))
        plt.plot(rounded_results_as_balance_change)
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title('Balance change over specified date range')
        plt.grid(axis='y')


plot_line_chart_balance_change(rounded_results_as_balance_change_to_chart_profits)


#  P/L LINE CHART
def plot_line_chart_profits_losses(rounded_trades_list):

    on_off = True

    if on_off:
        plt.figure(figsize=(15, 8))
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


def highlight_signal_on_chart(df):
    on_off = False   # To disable printing Line chart signals set to False

    if on_off:
        for i, s in enumerate(recognized_pattern):
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


highlight_signal_on_chart(filtered_by_date_dataframe)


#  CANDLESTICK CHART
def plot_candlestick_chart(df, signals):
    # warn_too_much_data = 200
    on_off = True

    if on_off:
        df.set_index('Datetime', inplace=True)

        add_plots = []  # Prepare additional plots
        # Add signals if provided
        # print(add_plots)
        # print(signals)

        signals_with_nan = signals.where(signals != 0, np.nan)  # replace values where the condition is False

        for i, s in enumerate(signals):     # Iterate over signals and add non-zero signals to add_plots
            if s != 0:
                # Add the signals as a subplot
                add_plots.append(mpf.make_addplot(signals_with_nan,
                                                  type='scatter', color='black', markersize=250, marker='+', panel=1))
                # Plot candlestick chart with additional plot
                # print(add_plots)
            else:
                pass
        print()
        print('Candlestick chart plotted')
        mpf.plot(df, type='candle', figsize=(15, 8), title=f'{file_path}'.upper(), ylabel='Price', addplot=add_plots,
                 warn_too_much_data=5000)


plot_candlestick_chart(filtered_by_date_dataframe, recognized_pattern)


plt.show()
