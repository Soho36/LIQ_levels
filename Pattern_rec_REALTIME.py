import talib
import time
import pandas as pd
import subprocess
import winsound

current_time = time.strftime('%H:%M:%S')


log_file_reading_interval = 1       # File reading interval (sec)
number_of_pattern = 22

# ************************************** ORDER PARAMETERS *******************************************************

volume_value = 0.01                 # 1000 MAX for stocks. Used only in AU3 (MT5 assigns volume itself)
risk_reward = 1                     # Risk/Reward ratio
sleep = 200                         # Pause between switching fields in MT5 order submit window
stop_loss_offset = 15               # Is added to SL for Shorts and subtracted for Longs (can be equal to spread)

# ***************************************************************************************************************
# Line numbers to be replaced in AU3 file
line_number_direction_buy_or_sell = 3
line_number_volume = 4
line_number_stop = 5
line_number_take = 6
line_number_sleep = 7

# New lines to replace with (new lines for SL and TP are in BUY/SELL logic blocks)
new_line_volume = f'Local $volume = {volume_value} ;replaceable line' + '/n'
new_line_sleep = f'Local $sleep = {sleep} ;replaceable line' + '/n'
# **************************************************************************************************************

# +------------------------------------------------------------------+
# FILE TRANSMIT PATHS
# +------------------------------------------------------------------+

order_send_by_ea_or_au3 = False         # True for AU3, False for EA

mt5_account_number = 258    # LAST 3 DIGITS OF MT5 ACCOUNT. MUST BE CHANGED BEFORE EXE BUILD

# MT5 directory with OHLC log file (logging on active timeframe):
mt5_logging_file_path = (
    f'C:/Users/Liikurserv/AppData/Roaming/MetaQuotes/Terminal/'
    f'30B7687250B3662E635CFEBC979C306C/MQL5/Files/'    # LONG FOLDER MUST BE CHANGED BEFORE EXE BUILD
    f'OHLCVData_{mt5_account_number}.csv'
)

# Autoit script for manual trade simulation
autoit_script_path = f'AU3/MT5_GUI_{mt5_account_number}.au3'

# File with signal generated by Python script
buy_sell_signals_for_mt5_filepath = (
     f'C:/Users/Liikurserv/AppData/Roaming/MetaQuotes/Terminal/'
     f'30B7687250B3662E635CFEBC979C306C/MQL5/Files/'    # LONG FOLDER MUST BE CHANGED BEFORE EXE BUILD
     f'buy_sell_signals_from_python_{number_of_pattern}.txt'
     )

try:
    buy_signal_discovered = False                   # MUST BE FALSE BEFORE ENTERING MAIN LOOP
    sell_signal_discovered = False                  # MUST BE FALSE BEFORE ENTERING MAIN LOOP

    while True:                                     # Main loop beginning

        # +------------------------------------------------------------------+
        # DATAFRAME CREATION
        # +------------------------------------------------------------------+
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

        patterns_dataframe = pd.read_csv('Ta-lib patterns.csv')

        # +------------------------------------------------------------------+
        # PATTERN RECOGNITION
        # +------------------------------------------------------------------+

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
            # pattern_signal_list = [0, 0, 0, 0, 0, -100]
            # pattern_signal = pd.Series(pattern_signal_list)     # hardcoded a series for debugging

            print(f'Pattern signals (last 10): {list(pattern_signal)[-10:]}')

            # +------------------------------------------------------------------+
            # BUY ORDER LOGIC
            # +------------------------------------------------------------------+
            # +------------------------------------------------------------------+
            # Replacing lines in AU3 file. Manual order entry simulation
            # +------------------------------------------------------------------+

            if order_send_by_ea_or_au3:

                if pattern_signal.iloc[-1] == 0:    # Set Flags to False after signal has been discovered
                    buy_signal, sell_signal = False, False

                if pattern_signal.iloc[-1] == 100 and not buy_signal:
                    winsound.PlaySound('chord.wav', winsound.SND_FILENAME)
                    print()
                    print('▲ ▲ ▲ Buy signal discovered! ▲ ▲ ▲'.upper())
                    buy_or_sell_flag = True            # bool for AU3 file. True for "BUY", False for "SELL"

                    # ****************************   ORDER PARAMETERS   ****************************
                    stop_loss_price = round(last_candle_low - stop_loss_offset, 3)
                    take_profit_price = round((((last_candle_close - stop_loss_price) *
                                                risk_reward) + last_candle_close) + stop_loss_offset, 3)
                    new_line_direction_buy_or_sell = (f'Local $trade_direction_buy_or_sell = '
                                                      f'{buy_or_sell_flag} ;replaceable line. '
                                                      f'True for BUY, False for Sell') + '/n'
                    new_line_stop = f'Local $stop_loss = {stop_loss_price} ;replaceable line' + '/n'
                    new_line_take = f'Local $take_profit = {take_profit_price} ;replaceable line' + '/n'

                    # +------------------------------------------------------------------+
                    # AU3 READING/WRITING FOR LONGS
                    # +------------------------------------------------------------------+

                    with open(autoit_script_path, 'r') as file:                        # Reading current au3.file
                        lines = file.readlines()
                    lines[line_number_volume - 1] = new_line_volume
                    lines[line_number_stop - 1] = new_line_stop
                    lines[line_number_take - 1] = new_line_take
                    lines[line_number_direction_buy_or_sell - 1] = new_line_direction_buy_or_sell
                    lines[line_number_sleep - 1] = new_line_sleep

                    with open(autoit_script_path, 'w') as file:                        # Writing au3.file with new lines
                        file.writelines(lines)

                    try:
                        subprocess.run(['start', autoit_script_path], shell=True)
                        print('AutoIt script executed successfully BUY')
                    except subprocess.CalledProcessError as e:
                        print(f'Error executing AutoIt script BUY: {e}')

                    buy_signal = True   # Setting flag back to TRUE

            # +------------------------------------------------------------------+
            # Creating file for MT5 to read
            # +------------------------------------------------------------------+

            else:

                if pattern_signal.iloc[-1] == 0:    # Set Flags to False after signal has been discovered
                    buy_signal, sell_signal = False, False

                if pattern_signal.iloc[-1] == 100 and not buy_signal:
                    winsound.PlaySound('chord.wav', winsound.SND_FILENAME)
                    print()
                    print('▲ ▲ ▲ Buy signal discovered! ▲ ▲ ▲'.upper())

                    # ORDER PARAMETERS
                    stop_loss_price = round(last_candle_low - stop_loss_offset, 3)
                    take_profit_price = round((((last_candle_close - stop_loss_price)
                                                * risk_reward) + last_candle_close) + stop_loss_offset, 3)

                    line_order_parameters = f'{ticker},Buy,{stop_loss_price},{take_profit_price}'

                    with open(buy_sell_signals_for_mt5_filepath, 'w', encoding='utf-8') as file:
                        file.writelines(line_order_parameters)

                    buy_signal = True  # Setting flag back to TRUE

            # +------------------------------------------------------------------+
            # SELL ORDER LOGIC
            # +------------------------------------------------------------------+
            # +------------------------------------------------------------------+
            # Replacing lines in AU3 file. Manual order entry simulation
            # +------------------------------------------------------------------+
            if order_send_by_ea_or_au3:

                if pattern_signal.iloc[-1] == 0:    # Set Flags to False after signal has been discovered
                    buy_signal, sell_signal = False, False

                if pattern_signal.iloc[-1] == -100 and not sell_signal:

                    winsound.PlaySound('chord.wav', winsound.SND_FILENAME)
                    print()
                    print('▼ ▼ ▼ Sell signal discovered! ▼ ▼ ▼'.upper())
                    buy_or_sell_flag = False            # Bool for AU3 file. True for "BUY", False for "SELL"

                    # ****************************   ORDER PARAMETERS   ****************************
                    stop_loss_price = round(last_candle_high + stop_loss_offset, 3)
                    take_profit_price = round((last_candle_close - ((stop_loss_price - last_candle_close) *
                                                                    risk_reward)) + stop_loss_offset, 3)
                    new_line_direction_buy_or_sell = (f'Local $trade_direction_buy_or_sell = '
                                                      f'{buy_or_sell_flag} ;replaceable line. '
                                                      f'True for BUY, False for Sell') + '/n'
                    new_line_stop = f'Local $stop_loss = {stop_loss_price} ;replaceable line' + '/n'
                    new_line_take = f'Local $take_profit = {take_profit_price} ;replaceable line' + '/n'

                    # +------------------------------------------------------------------+
                    # AU3 READING/WRITING FOR SHORTS
                    # +------------------------------------------------------------------+

                    with open(autoit_script_path, 'r') as file:                         # Reading current au3.file
                        lines = file.readlines()
                        # print(lines)
                    lines[line_number_volume - 1] = new_line_volume
                    lines[line_number_stop - 1] = new_line_stop
                    lines[line_number_take - 1] = new_line_take
                    lines[line_number_direction_buy_or_sell - 1] = new_line_direction_buy_or_sell
                    lines[line_number_sleep - 1] = new_line_sleep

                    with open(autoit_script_path, 'w') as file:                        # Writing au3.file with new lines
                        file.writelines(lines)

                    try:
                        subprocess.run(['start', autoit_script_path], shell=True)
                        print('AutoIt script executed successfully SELL')
                    except subprocess.CalledProcessError as e:
                        print(f'Error executing AutoIt script SELL: {e}')

                    sell_signal = True  # Setting flag back to TRUE

            # +------------------------------------------------------------------+
            # Creating file for MT5 to read
            # +------------------------------------------------------------------+
            else:

                if pattern_signal.iloc[-1] == 0:  # Set Flags to False after signal has been discovered
                    buy_signal, sell_signal = False, False

                if pattern_signal.iloc[-1] == -100 and not sell_signal:
                    winsound.PlaySound('chord.wav', winsound.SND_FILENAME)
                    print()
                    print('▼ ▼ ▼ Sell signal discovered! ▼ ▼ ▼'.upper())

                    # ORDER PARAMETERS
                    stop_loss_price = round(last_candle_high + stop_loss_offset)
                    take_profit_price = round((last_candle_close - ((stop_loss_price - last_candle_close) *
                                                                    risk_reward)) + stop_loss_offset, 3)

                    line_order_parameters = f'{ticker},Sell,{stop_loss_price},{take_profit_price}'

                    with open(buy_sell_signals_for_mt5_filepath, 'w', encoding='utf-8') as file:
                        file.writelines(line_order_parameters)

                    sell_signal = True  # Setting flag back to TRUE

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
