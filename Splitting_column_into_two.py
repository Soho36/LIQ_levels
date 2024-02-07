import pandas as pd

df = pd.read_csv('TXT/MT4/BTCUSD_m5.csv', parse_dates=[0])

print(df.head())
print(df['Date'].dtype)

df['Date2'] = df['Date'].dt.date
df['Time'] = df['Date'].dt.time

df.insert(1, 'Time', df.pop('Time'))
df.insert(0, 'Date2', df.pop('Date2'))
#
df.drop('Date', axis=1, inplace=True)

df.rename(columns={'Date2': 'Date'}, inplace=True)

df.to_csv('TXT/MT4/BTCUSD_m5.csv', index=False)

print(df.info())
print(df.head())
