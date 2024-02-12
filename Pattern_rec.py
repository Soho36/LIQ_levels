import talib
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
# from matplotlib.dates import date2num


#  ----------------------------------------------
#  MERGING FILES HERE. COMMENT OUT IF NECESSARY
#  ----------------------------------------------

def merging_files():

    need_merge = False

    if need_merge:
        folder_path = 'TXT'
        file_pattern = f'{folder_path}/*.csv'
        file_list = glob.glob(file_pattern)
        print('Files list: ', file_list)

        # Creating dataframe from multiple CVS-s in order to add last column Filename
        data_frames = [pd.read_csv(file).assign(Filename=file) for file in file_list]
        print('Dataframes from each csv: ', data_frames)

        for file, dataframe in zip(file_list, data_frames):       # Writing dataframe to each CSV
            dataframe_from_csv.to_csv(file, index=False)

        merged_df = pd.concat(data_frames, ignore_index=True)
        print('Merged dataframes: ', merged_df.head())

        merged_df.to_csv(f'TXT/merged_data.csv', index=False)  # Writing merged CSV


merging_files()

directory_path = 'TXT/'  # Making a list of files in TXT folder
file_names = []
for filename in os.listdir(directory_path):
    file_names.append(filename)
print('\nDatafiles in folder: ', file_names)

# file_path = 'TXT/merged_data.csv'
# file_path = 'TXT/exel.csv'
# file_path = 'TXT/spr.csv'
# file_path = 'TXT/zim.csv'
# file_path = 'TXT/extr.csv'
# file_path = 'TXT/aehr.csv'
# file_path = 'TXT/neog.csv'
# file_path = 'TXT/tsla_D1.csv'
# file_path = 'TXT/neog_D1.csv'
# file_path = 'TXT/meta_D1.csv'
# file_path = 'TXT/tsla_m5.csv'
# file_path = 'TXT/tsla_m1.csv'
# file_path = 'TXT/MT4/BTCUSD_D1.csv'
# file_path = 'TXT/MT4/BTCUSD60.csv'
file_path = 'TXT/MT4/BTCUSD_m5.csv'


print('\nCurrent file is: ', file_path)

columns_to_parce = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Filename']

#  for MT4 files set dayfirst=False
dataframe_from_csv = pd.read_csv(file_path, parse_dates=[0], dayfirst=False, usecols=columns_to_parce)
print('\nDataframe derived from CSV: \n', dataframe_from_csv.head())


# Parsing date range
def date_range_func(df):

    on_off = True

    if on_off:
        start_date = '2023-06-23'
        end_date = '2023-11-25'

        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        print('Date range: \n', list(date_range))

        date_column = df['Date']        # Select the 'Date' column from the DataFrame
        dates_in_range = date_column.isin(date_range)   # checks which dates from date_column fall within the generated
        # date range, resulting in a boolean mask

        df_filtered_by_date = df[dates_in_range]
        return df_filtered_by_date


filtered_by_date_dataframe = date_range_func(dataframe_from_csv)
print('Filtered by date dataframe: \n', filtered_by_date_dataframe)


#  ----------------------------------------------
#  PATTERN RECOGNITION
#  ----------------------------------------------

patterns_dataframe = pd.read_csv('Ta-lib patterns.csv')


def pattern_recognition_func(patterns_df):  # Reading Pattern codes from CSV

    idx = 16     # Choose the index of pattern here (from Ta-lib patterns.csv)
    pattern_code = patterns_df['PatternCode'].iloc[idx]
    pattern_name = patterns_df['PatternName'].iloc[idx]
    print('Current Pattern is: ', pattern_code, pattern_name)

    pattern_function = getattr(talib, pattern_code)
    signal = pattern_function(filtered_by_date_dataframe['Open'], filtered_by_date_dataframe['High'],
                              filtered_by_date_dataframe['Low'], filtered_by_date_dataframe['Close'])

    return signal


recognized_pattern = pattern_recognition_func(patterns_dataframe)
# Print the signals if any


def print_signals_to_cmd():

    on_off = False

    if on_off:
        for i, s in enumerate(recognized_pattern):
            if s == 100:
                print("Signal bullish:", i, s)
            elif s == -100:
                print("Signal bearish:", i, s)


print_signals_to_cmd()


#  ----------------------------------------------
#  PLOT CHART
#  ----------------------------------------------

#  Adding datetime column to dataframe

filtered_by_date_dataframe = (filtered_by_date_dataframe.assign(
    Datetime=(filtered_by_date_dataframe['Date'] + pd.to_timedelta(filtered_by_date_dataframe['Time']))))


def plot_chart(df):
    on_off = True

    if on_off:
        plt.figure(figsize=(15, 8))
        plt.plot(df['Datetime'], df['Close'], label='Ticker prices', marker='o')
        plt.title(f'{file_path}'.upper())
        plt.xlabel('Index')
        plt.ylabel('Price')
        plt.legend()


plot_chart(filtered_by_date_dataframe)

# Converting to numeric dates in order to plot multiple charts within the same dates range
# numeric_dates = date2num(df_csv['Datetime'])
# print('numeric_dates', numeric_dates)
# Converting numeric dates back to daytime in order to print a date Signal occurred


#  ----------------------------------------------
#  HIGHLIGHT SIGNALS
#  ----------------------------------------------


date_time_dates = pd.to_datetime(filtered_by_date_dataframe['Datetime'])
print('Date_time_dates: \n', date_time_dates)


def highlight_signal_on_chart(df):
    on_off = True

    if on_off:
        for i, s in enumerate(recognized_pattern):
            if s == 100:
                signal_date = df['Datetime'].iloc[i].strftime("%d-%m-%Y-%H-%M")
                file_name = df['Filename'].iloc[i]
                annotation_text = f'Bullish signal on {signal_date} in {file_name}'
                # the point where the arrow will be pointing to:
                plt.annotate(annotation_text, xy=(df['Datetime'].iloc[i], df['Close'].iloc[i]),
                             xytext=(df['Datetime'].iloc[i], df['Close'].iloc[i] + 100),
                             arrowprops=dict(arrowstyle='->'))
            elif s == -100:
                signal_date = df['Datetime'].iloc[i].strftime("%d-%m-%Y-%H-%M")
                annotation_text = f'Bearish signal on {signal_date} {file_path}'
                plt.annotate(annotation_text, xy=(df['Datetime'].iloc[i], df['Close'].iloc[i]),
                             xytext=(df['Datetime'].iloc[i], df['Close'].iloc[i] + 100),
                             arrowprops=dict(arrowstyle='->'))


highlight_signal_on_chart(filtered_by_date_dataframe)

plt.show()
