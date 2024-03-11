import time
import pandas as pd
# import mplfinance as mpf
# import pandas.errors


file_path = ('C:/Users/Liikurserv/AppData/Roaming/MetaQuotes/Terminal/010E047102812FC0C18890992854220E/MQL5/'
             'Logs/20240312.log')

log_file_reading_interval = 2

try:
    while True:
        def get_dataframe_from_file():
            log_df = pd.read_csv(file_path, sep='[\t;]', encoding='utf-16', engine='python')
            return log_df


        dataframe_from_log = get_dataframe_from_file()

        # print('Dataframe derived:')
        # print(dataframe_from_log)

        new_column_names = ['1', '2', 'Time', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']
        dataframe_from_log.columns = new_column_names

        # print(log_dataframe)

        columns_to_drop = ['1', '2', 'Volume']
        dataframe_from_log = dataframe_from_log.drop(columns=columns_to_drop)
        print('Modified dataframe:')
        print(dataframe_from_log)

        daytime = pd.to_datetime(dataframe_from_log['Time'], format='mixed')
        print('Converted daytime')
        print(daytime)
        dataframe_from_log = dataframe_from_log.assign(Datetime=daytime)
        dataframe_from_log = dataframe_from_log.drop(columns='Time')
        print(dataframe_from_log)

        time.sleep(log_file_reading_interval)
except KeyboardInterrupt:
    print('Program stopped manually')

# def plot_candlestick_chart():
#
#     dataframe_from_log.set_index('Datetime', inplace=True)
#     try:
#         mpf.plot(dataframe_from_log, type='candle', figsize=(10, 6), title='Candlestick chart', ylabel='Price')
#     except IndexError:
#         print('Empty DataFrame')
#
#
# plot_candlestick_chart()
