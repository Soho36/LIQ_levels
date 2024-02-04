import talib
import pandas as pd
import glob
import matplotlib.pyplot as plt
from matplotlib.dates import date2num


file_pattern = '*.txt'
file_list = glob.glob(file_pattern)
print('Files list: ', file_list)

data_frames = [pd.read_csv(file) for file in file_list]
print('Dataframes from each csv: ', data_frames)

merged_df = pd.concat(data_frames, ignore_index=True)
print('Merged dataframes: ', merged_df)


merged_df.to_csv(f'merged_data.csv', index=False)

file_path = 'merged_data.csv'
# file_path = 'exel.txt'
# file_path = 'spr.txt'
# file_path = 'zim.txt'
# file_path = 'extr.txt'
# file_path = 'aehr.txt'

columns_to_parce = ['Date', 'Open', 'High', 'Low', 'Close']

df = pd.read_csv(file_path, parse_dates=[0], dayfirst=True, usecols=columns_to_parce, index_col=0)
print('Dataframe from merged csv: ', df)

# Converting to numeric dates in order to plot multiple charts within the same dates range
numeric_dates = date2num(df.index)
print('Numeric dates: ', numeric_dates)


# Pattern type
signal = talib.CDL3OUTSIDE(df['Open'], df['High'], df['Low'], df['Close'])
print(list(enumerate(signal)))

# Print the signals
for i, s in enumerate(signal):
    if s == 100:
        print("Signal bullish:", s)
    elif s == -100:
        print("Signal bearish:", s)

# Plot chart
plt.figure(figsize=(15, 8))
plt.plot(numeric_dates, df['Close'], label='Stock Prices', marker='o')
plt.title('Line chart')
plt.xlabel('Index')
plt.ylabel('Price')
plt.legend()


# Converting numeric dates back to daytime in order to print a date Signal occurred
date_time_dates = pd.to_datetime(numeric_dates, unit='D')
print('date_time_dates: ', date_time_dates)


# Highlight signals
for i, s in enumerate(signal):
    if s == 100:
        signal_date = date_time_dates[i].strftime("%d-%m-%Y-%H-%M")
        annotation_text = f'Bullish signal on {signal_date}'
        plt.annotate(annotation_text, xy=(numeric_dates[i], df['Close'].iloc[i]),
                     xytext=(numeric_dates[i], df['Close'].iloc[i] + 1),
                     arrowprops=dict(arrowstyle='->'))
    elif s == -100:
        signal_date = date_time_dates[i].strftime("%d-%m-%Y-%H-%M")
        annotation_text = f'Bearish signal on {signal_date}'
        plt.annotate(annotation_text, xy=(numeric_dates[i], df['Close'].iloc[i]),
                     xytext=(numeric_dates[i], df['Close'].iloc[i] + 1),
                     arrowprops=dict(arrowstyle='->'))


plt.show()
