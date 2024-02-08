import pandas as pd

# df = pd.read_csv('TXT/MT4/BTCUSD60.csv', parse_dates=[0])
df = pd.read_csv('../BTCUSD60.csv', parse_dates=[0])

print(df.head())
