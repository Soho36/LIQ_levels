import time
import pandas as pd
import mplfinance as mpf
# import pandas.errors

# The path to MT5 directory containing log file:
file_path = ('C:/Users/Liikurserv/AppData/Roaming/MetaQuotes/Terminal/010E047102812FC0C18890992854220E/MQL5/Files/'
             'OHLCVData.csv')


log_file_reading_interval = 5   # File reading interval (sec)

try:
    while True:     # Creating a loop for refreshing intervals
        def get_dataframe_from_file():
            log_df = pd.read_csv(file_path, sep=';', encoding='utf-16', engine='python')
            return log_df

        dataframe_from_log = get_dataframe_from_file()

        new_column_names = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']  # Assigning columns names
        dataframe_from_log.columns = new_column_names

        daytime = pd.to_datetime(dataframe_from_log['Time'], format='mixed')    # Converting to DateTime format

        dataframe_from_log = dataframe_from_log.assign(Datetime=daytime)    # Insert Datetime column and...
        dataframe_from_log = dataframe_from_log.drop(columns='Time')    # deleting old 'Time' column
        print('Working dataframe:')
        print(dataframe_from_log)   # Printing the DataFrame to see whether it looks like as supposed to

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
