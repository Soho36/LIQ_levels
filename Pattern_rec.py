import talib
import pandas as pd
import os
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
# ------------------------------------------
# The list of paths to datafiles:
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
# ------------------------------------------
start_date = '2024-01-01'     # Choose the start date to begin from
end_date = '2024-01-02'     # Choose the end date
code_of_pattern = 9     # Choose the index of pattern (from Ta-lib patterns.csv)


def getting_dataframe_from_file(path):

    directory_path = 'TXT/'
    print('\nDatafiles in folder: ')
    for filename in os.listdir(directory_path):     # Making a list of files located in TXT folder
        print(filename)

    print('\nCurrent file is: ', path)

    columns_to_parce = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Filename']

    #  for MT4 files set dayfirst=False
    csv_df = pd.read_csv(path, parse_dates=[0], dayfirst=False, usecols=columns_to_parce)
    print('\nDataframe derived from CSV: \n', csv_df.head())
    return csv_df


dataframe_from_csv = getting_dataframe_from_file(file_path)


def date_range_func(df, start, end):

    on_off = True

    if on_off:
        date_range = pd.date_range(start=start, end=end, freq='D')
        # print('Date range: \n', list(date_range))

        date_column = df['Date']        # Select the 'Date' column from the DataFrame
        dates_in_range = date_column.isin(date_range)   # checks which dates from date_column fall within the generated
        # date range, resulting in a boolean mask

        df_filtered_by_date = df[dates_in_range]
        return df_filtered_by_date


filtered_by_date_dataframe = date_range_func(dataframe_from_csv, start_date, end_date)
print('Filtered by date dataframe: \n', filtered_by_date_dataframe)


#  ----------------------------------------------
#  PATTERN RECOGNITION
#  ----------------------------------------------

patterns_dataframe = pd.read_csv('Ta-lib patterns.csv')


def pattern_recognition_func(patterns_df, code):  # Reading Pattern codes from CSV

    pattern_code = patterns_df['PatternCode'].iloc[code]
    pattern_name = patterns_df['PatternName'].iloc[code]
    print('Current Pattern is: ', pattern_code, ',', pattern_name)

    pattern_function = getattr(talib, pattern_code)
    signal = pattern_function(filtered_by_date_dataframe['Open'], filtered_by_date_dataframe['High'],
                              filtered_by_date_dataframe['Low'], filtered_by_date_dataframe['Close'])

    return signal


recognized_pattern = pattern_recognition_func(patterns_dataframe, code_of_pattern)
# Print the signals if any


def print_signals_to_cmd():

    on_off = True

    if on_off:
        for i, s in enumerate(recognized_pattern):
            if s == 100:
                print("\nSignal bullish", "Index:", i,  "Value:", s)
            elif s == -100:
                print("\nSignal bearish", "Index:", i, "Value:", s)


print_signals_to_cmd()


#  ----------------------------------------------
#  PLOT CHART
#  ----------------------------------------------

#  Adding datetime column to dataframe
filtered_by_date_dataframe = (filtered_by_date_dataframe.assign(
    Datetime=(filtered_by_date_dataframe['Date'] + pd.to_timedelta(filtered_by_date_dataframe['Time']))))


def plot_line_chart(df):
    on_off = True   # To disable printing chart set to False

    if on_off:
        plt.figure(figsize=(15, 8))
        plt.plot(df['Datetime'], df['Close'], label='Ticker prices', marker='o')
        plt.title(f'{file_path}'.upper())
        plt.xlabel('Index')
        plt.ylabel('Price')
        plt.legend()


plot_line_chart(filtered_by_date_dataframe)


#  ----------------------------------------------
#  HIGHLIGHT SIGNALS
#  ----------------------------------------------


# date_time_dates = pd.to_datetime(filtered_by_date_dataframe['Datetime'])
# print('Date_time_dates: \n', date_time_dates)


def highlight_signal_on_chart(df):
    on_off = True   # To disable printing signals set to False

    if on_off:
        for i, s in enumerate(recognized_pattern):
            if s == 100:
                signal_date = df['Datetime'].iloc[i].strftime("%d-%m-%Y-%H-%M")
                file_name = df['Filename'].iloc[i]
                annotation_text = f'Bullish signal on {signal_date} in {file_name}'
                # the point where the arrow will be pointing to:
                plt.annotate(annotation_text,
                             xy=(df['Datetime'].iloc[i], df['Close'].iloc[i]),
                             xytext=(df['Datetime'].iloc[i], df['Close'].iloc[i] + 100),
                             arrowprops=dict(arrowstyle='->')
                             )
            elif s == -100:
                signal_date = df['Datetime'].iloc[i].strftime("%d-%m-%Y-%H-%M")
                annotation_text = f'Bearish signal on {signal_date} {file_path}'
<<<<<<< HEAD
                # the point where the arrow will be pointing to:
                plt.annotate(annotation_text, xy=(df['Datetime'].iloc[i], df['Close'].iloc[i]),
=======
                plt.annotate(annotation_text,
                             xy=(df['Datetime'].iloc[i], df['Close'].iloc[i]),
>>>>>>> candlestick
                             xytext=(df['Datetime'].iloc[i], df['Close'].iloc[i] + 100),
                             arrowprops=dict(arrowstyle='->')
                             )


highlight_signal_on_chart(filtered_by_date_dataframe)


def plot_candlestick_chart(df, signals):
    on_off = True

    if on_off:
        df.set_index('Datetime', inplace=True)

        add_plots = []  # Prepare additional plots
        # Add signals if provided
        print(add_plots)
        print(signals)

        signals_with_nan = signals.where(signals != 0, np.nan)  # replace values where the condition is False

        for i, s in enumerate(signals):     # Iterate over signals and add non-zero signals to add_plots
            if s != 0:
                # Add the signals as a subplot
                add_plots.append(mpf.make_addplot(signals_with_nan,
                                                  type='scatter', color='black', markersize=250, marker='+', panel=0))
                # Plot candlestick chart with additional plot
                print(add_plots)

        mpf.plot(df, type='candle', figsize=(15, 8), title=f'{file_path}'.upper(), ylabel='Price', addplot=add_plots)
        print('Signals are plotted to candlestick chart')


plot_candlestick_chart(filtered_by_date_dataframe, recognized_pattern)


plt.show()
