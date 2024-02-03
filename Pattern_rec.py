import talib
import pandas as pd
import matplotlib.pyplot as plt


# m1 dataframes file
# file_path = 'ROK_D1.txt'
file_path = 'ROK_2_D1.txt'


df = pd.read_csv(file_path, parse_dates=[0], dayfirst=True, index_col=0)
print(df)


# Pattern type
signal = talib.CDL3OUTSIDE(df['Open'], df['High'], df['Low'], df['Close'])

# Print the signals
print("Signal:", signal)

# Plot the stock prices with signals
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Close'], label='Stock Prices', marker='o')
plt.title('Line chart')
plt.xlabel('Days')
plt.ylabel('Price')
plt.legend()

# Highlight signals
for date, s in zip(df.index, signal):
    if s > 0:
        plt.annotate(f'Signal here{df.loc[date]}', xy=(date, df.loc[date, 'Close']),
                     xytext=(date, df.loc[date, 'Close'] + 5),
                     arrowprops=dict(facecolor='red', arrowstyle='->'))


plt.show()
