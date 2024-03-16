import talib
import time
import pandas as pd
import mplfinance as mpf
import subprocess
# import sys

# import pandas.errors

current_time = time.strftime('%H:%M:%S')
# The path to MT5 directory containing log file:
mt5_logging_file_path = ('C:/Users/Liikurserv/AppData/Roaming/MetaQuotes/Terminal/010E047102812FC0C18890992854220E/'
                         'MQL5/Files/OHLCVData.csv')
# autoit_script_path = 'AU3/MT5_GUI_test.au3'
autoit_script_path = 'AU3/MT5_GUI_test.au3'
#  ********************************************************************************************************************
log_file_reading_interval = 5       # File reading interval (sec)
number_of_pattern = 51
#  ********************************************************************************************************************
# ************************************** MT5 TRANSMIT SETTINGS ********************************************************

volume_value = 0.01                # 1000 MAX for stocks
risk_reward = 2
sleep = 100

# *********************************************************************************************************************
# This block is responsible for replacing lines in AU3 script with modified lines reflecting ORDER settings
line_number_direction_buy_or_sell = 3
line_number_volume = 4
line_number_stop = 5
line_number_take = 6
line_number_sleep = 7
new_line_volume = f'Local $volume = {volume_value} ;replaceable line' + '\n'
new_line_sleep = f'Local $sleep = {sleep} ;replaceable line' + '\n'


try:
    buy_signal_discovered = False
    sell_signal_discovered = False

    while True:     # Creating a loop for refreshing intervals

        def get_dataframe_from_file():
            log_df = pd.read_csv(mt5_logging_file_path, sep=';', encoding='utf-16', engine='python')
            return log_df

        dataframe_from_log = get_dataframe_from_file()

        # Assigning columns names
        new_column_names = ['Ticker', 'Timeframe', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        dataframe_from_log.columns = new_column_names

        daytime = pd.to_datetime(dataframe_from_log['Time'], format='mixed')    # Converting to DateTime format

        dataframe_from_log = dataframe_from_log.assign(Datetime=daytime)    # Insert Datetime column and...
        dataframe_from_log = dataframe_from_log.drop(columns='Time')    # Deleting old 'Time' column
        # Last candle OHLC
        last_candle_open = dataframe_from_log['Open'].iloc[-1]
        last_candle_high = dataframe_from_log['High'].iloc[-1]
        last_candle_low = dataframe_from_log['Low'].iloc[-1]
        last_candle_close = dataframe_from_log['Close'].iloc[-1]

        print('Last Open', last_candle_open)
        print('Last High', last_candle_high)
        print('Last Low', last_candle_low)
        print('Last Close', last_candle_close)
        print('Working dataframe:')
        print(dataframe_from_log)   # Printing the DataFrame to see whether it looks like as supposed to

        patterns_dataframe = pd.read_csv('Ta-lib patterns.csv')


        def pattern_recognition(patterns_df, pattern_number, log_dataframe, buy_signal, sell_signal):
            pattern_code = patterns_df['PatternCode'].iloc[pattern_number]
            pattern_name = patterns_df['PatternName'].iloc[pattern_number]
            pattern_index = patterns_df.index[pattern_number]
            print()
            print(f'Current Pattern is: {pattern_code}, {pattern_name}, {pattern_index}')

            pattern_function = getattr(talib, pattern_code)
            pattern_signal = pattern_function(log_dataframe['Open'], log_dataframe['High'],
                                              log_dataframe['Low'], log_dataframe['Close'])
            # pattern_signal = [0, 0, 0, 0, 0, -100]
            print(f'Pattern signals: {list(pattern_signal)}')

            # if pattern_signal[-1] == 100 and not buy_signal:
            if pattern_signal.iloc[-1] == 100 and not buy_signal:
                print()
                print('▲ ▲ ▲ Buy signal discovered! ▲ ▲ ▲'.upper())
                buy_or_sell_flag = True            # True for "BUY", False for "SELL"
                stop_loss_price = last_candle_low
                take_profit_price = (((last_candle_close - last_candle_low) * risk_reward) + last_candle_close)
                new_line_direction_buy_or_sell = (f'Local $trade_direction_buy_or_sell = '
                                                  f'{buy_or_sell_flag} ;replaceable line. '
                                                  f'True for BUY, False for Sell') + '\n'
                new_line_stop = f'Local $stop_loss = {stop_loss_price} ;replaceable line' + '\n'
                new_line_take = f'Local $take_profit = {take_profit_price} ;replaceable line' + '\n'

                with open(autoit_script_path, 'r') as file:                         # Reading current au3.file
                    lines = file.readlines()
                lines[line_number_volume - 1] = new_line_volume
                lines[line_number_stop - 1] = new_line_stop
                lines[line_number_take - 1] = new_line_take
                lines[line_number_direction_buy_or_sell - 1] = new_line_direction_buy_or_sell
                lines[line_number_sleep - 1] = new_line_sleep

                with open(autoit_script_path, 'w') as file:                         # Writing au3.file with new lines
                    file.writelines(lines)

                try:
                    subprocess.run(['start', autoit_script_path], shell=True)
                    print('AutoIt script executed successfully BUY')
                except subprocess.CalledProcessError as e:
                    print(f'Error executing AutoIt script BUY: {e}')

                buy_signal = True   # Setting flag back to TRUE
            # if pattern_signal[-1] == -100 and not sell_signal:
            if pattern_signal.iloc[-1] == -100 and not sell_signal:
                print()
                print('▼ ▼ ▼ Sell signal discovered! ▼ ▼ ▼'.upper())
                buy_or_sell_flag = False            # True for "BUY", False for "SELL"
                stop_loss_price = last_candle_high
                take_profit_price = (last_candle_close - ((stop_loss_price - last_candle_close) * risk_reward))
                new_line_direction_buy_or_sell = (f'Local $trade_direction_buy_or_sell = '
                                                  f'{buy_or_sell_flag} ;replaceable line. '
                                                  f'True for BUY, False for Sell') + '\n'
                new_line_stop = f'Local $stop_loss = {stop_loss_price} ;replaceable line' + '\n'
                new_line_take = f'Local $take_profit = {take_profit_price} ;replaceable line' + '\n'

                with open(autoit_script_path, 'r') as file:                         # Reading current au3.file
                    lines = file.readlines()
                    # print(lines)
                lines[line_number_volume - 1] = new_line_volume
                lines[line_number_stop - 1] = new_line_stop
                lines[line_number_take - 1] = new_line_take
                lines[line_number_direction_buy_or_sell - 1] = new_line_direction_buy_or_sell
                lines[line_number_sleep - 1] = new_line_sleep

                with open(autoit_script_path, 'w') as file:                         # Writing au3.file with new lines
                    file.writelines(lines)

                try:
                    subprocess.run(['start', autoit_script_path], shell=True)
                    print('AutoIt script executed successfully SELL')
                except subprocess.CalledProcessError as e:
                    print(f'Error executing AutoIt script SELL: {e}')

                sell_signal = True  # Setting flag back to TRUE

            return buy_signal, sell_signal


        buy_signal_discovered, sell_signal_discovered = (
            pattern_recognition(patterns_dataframe, number_of_pattern, dataframe_from_log,
                                buy_signal_discovered, sell_signal_discovered)
        )

        time.sleep(log_file_reading_interval)   # Pause between reading


except KeyboardInterrupt:
    print()
    print('Program stopped manually')   # Catching 'Stop' error

















#   PLOTTING CHART FUNCTIONALITY FOR THIS SCRIPT MOSTLY DISABLED

plot_candlestick_chart = False

if plot_candlestick_chart:
    def plot_candlestick_chart():

        dataframe_from_log.set_index('Datetime', inplace=True)
        try:
            mpf.plot(dataframe_from_log, type='candle', figsize=(10, 6), title='Candlestick chart', ylabel='Price')
        except IndexError:
            print('Empty DataFrame')


    plot_candlestick_chart()
else:
    print('Chart is switched off')
