import talib
import time
import pandas as pd
import subprocess
import winsound

current_time = time.strftime('%H:%M:%S')
# The path to MT5 directory containing log file:
mt5_logging_file_path = ('C:/Users/Liikurserv/AppData/Roaming/MetaQuotes/Terminal/09FF355D73768D9CE6BDD4EE575EAB09/'
                         'MQL5/Files/259_OHLCVData.csv')

autoit_script_path = 'AU3/MT5_GUI_167.au3'
buy_sell_signals_for_mt5_filepath = 'buy_sell_signals_for_mt5.txt'

order_send_ea_or_au3 = False         # True for EA, False for AU3
#  ********************************************************************************************************************
log_file_reading_interval = 2       # File reading interval (sec)
number_of_pattern = 15
#  ********************************************************************************************************************
# ************************************** MT5 TRANSMIT SETTINGS ********************************************************

volume_value = 0.01                 # 1000 MAX for stocks
risk_reward = 3                     # Risk/Reward ratio
sleep = 200                         # Pause between switching fields in MT5 order submit window
stop_loss_offset = 15               # Is added to SL for Shorts and subtracted for Longs (can be equal to spread)

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
    buy_signal_discovered = False                   # MUST BE FALSE BEFORE ENTERING MAIN LOOP
    sell_signal_discovered = False                  # MUST BE FALSE BEFORE ENTERING MAIN LOOP
    print('Before entering loop buy: ', buy_signal_discovered)
    print('Before entering loop sell: ', sell_signal_discovered)

    while True:                                     # Creating a loop for refreshing intervals

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
        try:
            last_candle_open = dataframe_from_log['Open'].iloc[-1]
            last_candle_high = dataframe_from_log['High'].iloc[-1]
            last_candle_low = dataframe_from_log['Low'].iloc[-1]
            last_candle_close = dataframe_from_log['Close'].iloc[-1]
            ticker = dataframe_from_log['Ticker'].iloc[-1]
        except IndexError:
            print("Must be at least two rows in the source file")

        # print('Last Open', last_candle_open)
        # print('Last High', last_candle_high)
        # print('Last Low', last_candle_low)
        # print('Last Close', last_candle_close)
        # print(Working dataframe:)
        # print(dataframe_from_log)   # Printing the DataFrame to see whether it looks like as supposed to

        patterns_dataframe = pd.read_csv('Ta-lib patterns.csv')


        def pattern_recognition(patterns_df, pattern_number, log_dataframe, buy_signal, sell_signal):
            pattern_code = patterns_df['PatternCode'].iloc[pattern_number]
            pattern_name = patterns_df['PatternName'].iloc[pattern_number]
            pattern_index = patterns_df.index[pattern_number]
            time_frame = dataframe_from_log['Timeframe'].iloc[-1]
            print('--------------------------------------------------------------------')
            print(f'Current Pattern is: {pattern_code}, {pattern_name}, {pattern_index}, {time_frame}')

            pattern_function = getattr(talib, pattern_code)
            pattern_signal = pattern_function(log_dataframe['Open'], log_dataframe['High'],
                                              log_dataframe['Low'], log_dataframe['Close'])
            pattern_signal = [0, 0, 0, 0, 0, 100]
            # print(f'Pattern signals (last 10): {list(pattern_signal)[-10:]}')

            # +------------------------------------------------------------------+
            # BUY ORDER LOGIC
            # +------------------------------------------------------------------+
            if order_send_ea_or_au3:
                if pattern_signal[-1] == 100 and not buy_signal:
                # print('Right before IF buy: ', buy_signal, 'Pattern signal: ', pattern_signal.iloc[-1])

                # if pattern_signal.iloc[-1] == 0:    # Set Flags to False after signal has been discovered
                #     buy_signal, sell_signal = False, False

                # if pattern_signal.iloc[-1] == 100 and not buy_signal:
                    winsound.PlaySound('chord.wav', winsound.SND_FILENAME)
                    print()
                    print('▲ ▲ ▲ Buy signal discovered! ▲ ▲ ▲'.upper())
                    buy_or_sell_flag = True            # True for "BUY", False for "SELL"

                    # ORDER PARAMETERS
                    stop_loss_price = last_candle_low - stop_loss_offset
                    take_profit_price = round((((last_candle_close - stop_loss_price) * risk_reward) +
                                               last_candle_close), 3)
                    new_line_direction_buy_or_sell = (f'Local $trade_direction_buy_or_sell = '
                                                      f'{buy_or_sell_flag} ;replaceable line. '
                                                      f'True for BUY, False for Sell') + '\n'
                    new_line_stop = f'Local $stop_loss = {stop_loss_price} ;replaceable line' + '\n'
                    new_line_take = f'Local $take_profit = {take_profit_price} ;replaceable line' + '\n'
                    # Line with order parameters to write to MT5 file for trade placement EA
                    line_order_parameters = f'{ticker},Buy,{stop_loss_price},{take_profit_price}'

                    with open(autoit_script_path, 'r') as file:                         # Reading current au3.file
                        lines = file.readlines()
                    lines[line_number_volume - 1] = new_line_volume
                    lines[line_number_stop - 1] = new_line_stop
                    lines[line_number_take - 1] = new_line_take
                    lines[line_number_direction_buy_or_sell - 1] = new_line_direction_buy_or_sell
                    lines[line_number_sleep - 1] = new_line_sleep

                    with open(autoit_script_path, 'w') as file:                         # Writing au3.file with new lines
                        file.writelines(lines)

                    with open(buy_sell_signals_for_mt5_filepath, 'w', encoding='utf-8') as file:
                        file.writelines(line_order_parameters)

                    try:
                        subprocess.run(['start', autoit_script_path], shell=True)
                        print('AutoIt script executed successfully BUY')
                    except subprocess.CalledProcessError as e:
                        print(f'Error executing AutoIt script BUY: {e}')

                    buy_signal = True   # Setting flag back to TRUE
            else:
                if pattern_signal[-1] == 100 and not buy_signal:
                    # print('Right before IF buy: ', buy_signal, 'Pattern signal: ', pattern_signal.iloc[-1])

                    # if pattern_signal.iloc[-1] == 0:    # Set Flags to False after signal has been discovered
                    #     buy_signal, sell_signal = False, False

                    # if pattern_signal.iloc[-1] == 100 and not buy_signal:
                    winsound.PlaySound('chord.wav', winsound.SND_FILENAME)
                    print()
                    print('▲ ▲ ▲ Buy signal discovered! ▲ ▲ ▲'.upper())
                    buy_or_sell_flag = True  # True for "BUY", False for "SELL"

                    # ORDER PARAMETERS
                    stop_loss_price = last_candle_low - stop_loss_offset
                    take_profit_price = round((((last_candle_close - stop_loss_price) * risk_reward) +
                                               last_candle_close), 3)

                    line_order_parameters = f'{ticker},Buy,{stop_loss_price},{take_profit_price}'

                    with open(buy_sell_signals_for_mt5_filepath, 'w', encoding='utf-8') as file:
                        file.writelines(line_order_parameters)

                    buy_signal = True  # Setting flag back to TRUE

            # +------------------------------------------------------------------+
            # SELL ORDER LOGIC
            # +------------------------------------------------------------------+
            if order_send_ea_or_au3:
                # if pattern_signal[-1] == -100 and not sell_signal:

                    #print('Right before IF Sell: ', sell_signal, 'Pattern signal: ', pattern_signal.iloc[-1])


                if pattern_signal[-1] == -100 and not sell_signal:
                #if pattern_signal.iloc[-1] == -100 and not sell_signal:
                    print('Right inside IF sell: ', sell_signal)
                    winsound.PlaySound('chord.wav', winsound.SND_FILENAME)
                    print()
                    print('▼ ▼ ▼ Sell signal discovered! ▼ ▼ ▼'.upper())
                    buy_or_sell_flag = False            # True for "BUY", False for "SELL"
                    stop_loss_price = last_candle_high + stop_loss_offset
                    take_profit_price = round((last_candle_close - ((stop_loss_price - last_candle_close) *
                                                                    risk_reward)), 3)
                    new_line_direction_buy_or_sell = (f'Local $trade_direction_buy_or_sell = '
                                                      f'{buy_or_sell_flag} ;replaceable line. '
                                                      f'True for BUY, False for Sell') + '\n'
                    new_line_stop = f'Local $stop_loss = {stop_loss_price} ;replaceable line' + '\n'
                    new_line_take = f'Local $take_profit = {take_profit_price} ;replaceable line' + '\n'
                    line_order_parameters = f'{ticker},Buy,{stop_loss_price},{take_profit_price}'

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

                    with open(buy_sell_signals_for_mt5_filepath, 'w', encoding='utf-8') as file:
                        file.writelines(line_order_parameters)

                    try:
                        subprocess.run(['start', autoit_script_path], shell=True)
                        print('AutoIt script executed successfully SELL')
                    except subprocess.CalledProcessError as e:
                        print(f'Error executing AutoIt script SELL: {e}')
                    print('Line 155: ', sell_signal)
                    sell_signal = True  # Setting flag back to TRUE
                    print('Line 157: ', sell_signal)

                return buy_signal, sell_signal


        try:
            buy_signal_discovered, sell_signal_discovered = (
                pattern_recognition(patterns_dataframe, number_of_pattern, dataframe_from_log,
                                    buy_signal_discovered, sell_signal_discovered)
            )
        except IndexError:
            print('Must be at least two rows in the source file')

        time.sleep(log_file_reading_interval)   # Pause between reading


except KeyboardInterrupt:
    print()
    print('Program stopped manually')   # Catching 'Stop' error
