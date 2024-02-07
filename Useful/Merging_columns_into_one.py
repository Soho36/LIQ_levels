import pandas as pd

df = pd.read_csv('..TXT/MT4/BTCUSD_m5.csv', parse_dates=[0])
print(df.head())

df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df.insert(0, 'Datetime', df.pop('Datetime'))
df.drop(['Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0'], axis=1, inplace=True)  # axis=1 for columns, axis=2 for rows

df.to_csv('TXT/BTCUSD_m5.csv', index=False)
