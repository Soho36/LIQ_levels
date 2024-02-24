import pandas as pd
import os

# df = pd.read_csv('TXT/MT4/BTCUSD_m60.csv', parse_dates=[0])
df = pd.read_csv('../TXT/MT4/BTCUSD_m60.csv', parse_dates=[0])
print(df.head())
file_path = '../TXT/MT4/BTCUSD_m60.csv'
file_name = os.path.basename(file_path)

print('File name: ', file_name)

df = df.assign(Filename=file_name)

print(df.head())

on_off = True      # turn on and off
if on_off:
    df.to_csv('../TXT/MT4/BTCUSD_m60.csv', index=False)
else:
    pass


