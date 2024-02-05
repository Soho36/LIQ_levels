import talib
import pandas as pd
import glob
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

# Мerged files part
folder_path = 'TXT'
file_pattern = f'{folder_path}/*.txt'
file_list = glob.glob(file_pattern)
print('Files list: ', file_list)

# Creating dataframe from multiple CVS-s in order to add last column Filename
data_frames = [pd.read_csv(file).assign(Filename=file) for file in file_list]
print('Dataframes from each csv: ', data_frames)


for file, df in zip(file_list, data_frames):       # Writing dataframe to each CSV
    df.to_csv(file, index=False)

merged_df = pd.concat(data_frames, ignore_index=True)
print('Merged dataframes: ', merged_df)


merged_df.to_csv(f'TXT/merged_data.csv', index=False)  # Writing merged CSV

# End of the part for merged files

# file_path = 'TXT/merged_data.csv'
# file_path = 'TXT/exel.txt'
# file_path = 'TXT/spr.txt'
# file_path = 'TXT/zim.txt'
# file_path = 'TXT/extr.txt'
# file_path = 'TXT/aehr.txt'
# file_path = 'TXT/neog.txt'
# file_path = 'TXT/tsla_D1.txt'
file_path = 'TXT/neog_D1.txt'


columns_to_parce = ['Date', 'Open', 'High', 'Low', 'Close', 'Filename']

df = pd.read_csv(file_path, parse_dates=[0], dayfirst=True, usecols=columns_to_parce, index_col=0)
print('Dataframe from merged csv: ', df)


# Converting to numeric dates in order to plot multiple charts within the same dates range
numeric_dates = date2num(df.index)


# PATTERN TYPE

df_pattern = pd.read_csv('Ta-lib patterns.csv')  # Reading Pattern codes from CSV

idx = 2     # Choose the index of pattern here (from Ta-lib patterns.csv)
pattern_code = df_pattern['PatternCode'].iloc[idx]
pattern_name = df_pattern['PatternName'].iloc[idx]
print('Current Pattern is: ', pattern_code, pattern_name)

pattern_function = getattr(talib, pattern_code)
signal = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])


# Print the signals
for i, s in enumerate(signal):
    if s == 100:
        print("Signal bullish:", s)
    elif s == -100:
        print("Signal bearish:", s)

# Plot chart
plt.figure(figsize=(15, 8))
plt.plot(numeric_dates, df['Close'], label='Stock Prices', marker='o')
plt.title(f'{file_path}'.upper())
plt.xlabel('Index')
plt.ylabel('Price')
plt.legend()


# Converting numeric dates back to daytime in order to print a date Signal occurred
date_time_dates = pd.to_datetime(numeric_dates, unit='D')


# Highlight signals on the chart
for i, s in enumerate(signal):
    if s == 100:
        signal_date = date_time_dates[i].strftime("%d-%m-%Y-%H-%M")
        file_name = df['Filename'].iloc[i]
        annotation_text = f'Bullish signal on {signal_date} in {file_name}'
        plt.annotate(annotation_text, xy=(numeric_dates[i], df['Close'].iloc[i]),
                     xytext=(numeric_dates[i], df['Close'].iloc[i] + 0.1),
                     arrowprops=dict(arrowstyle='->'))
    elif s == -100:
        signal_date = date_time_dates[i].strftime("%d-%m-%Y-%H-%M")
        annotation_text = f'Bearish signal on {signal_date} {file_path}'
        plt.annotate(annotation_text, xy=(numeric_dates[i], df['Close'].iloc[i]),
                     xytext=(numeric_dates[i], df['Close'].iloc[i] + 0.1),
                     arrowprops=dict(arrowstyle='->'))


plt.show()
