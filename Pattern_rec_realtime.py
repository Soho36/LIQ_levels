import talib
import time
import pandas as pd
import mplfinance as mpf
# import pandas.errors

# The path to MT5 directory containing log file:
file_path = ('C:/Users/Liikurserv/AppData/Roaming/MetaQuotes/Terminal/010E047102812FC0C18890992854220E/MQL5/Files/'
             'OHLCVData.csv')

#  ********************************************************************************************************************
log_file_reading_interval = 5   # File reading interval (sec)
number_of_pattern = 51

#  ********************************************************************************************************************
try:
    buy_signal_discovered = False
    sell_signal_discovered = False

    while True:     # Creating a loop for refreshing intervals

        def get_dataframe_from_file():
            log_df = pd.read_csv(file_path, sep=';', encoding='utf-16', engine='python')
            return log_df

        dataframe_from_log = get_dataframe_from_file()

        # Assigning columns names
        new_column_names = ['Ticker', 'Timeframe', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        dataframe_from_log.columns = new_column_names

        daytime = pd.to_datetime(dataframe_from_log['Time'], format='mixed')    # Converting to DateTime format

        dataframe_from_log = dataframe_from_log.assign(Datetime=daytime)    # Insert Datetime column and...
        dataframe_from_log = dataframe_from_log.drop(columns='Time')    # deleting old 'Time' column
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
            print(f'Pattern signals: {list(pattern_signal)}')

            if pattern_signal.iloc[-1] == 100 and not buy_signal:
                print('Buy signal discovered!'.title())
                buy_signal = True
            if pattern_signal.iloc[-1] == -100 and not sell_signal:
                print('Sell signal discovered!'.title())
                sell_signal = True

            return buy_signal, sell_signal


        buy_signal_discovered, sell_signal_discovered = (
            pattern_recognition(patterns_dataframe, number_of_pattern, dataframe_from_log,
                                buy_signal_discovered, sell_signal_discovered)
        )

        time.sleep(log_file_reading_interval)   # Pause between reading


except KeyboardInterrupt:
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
