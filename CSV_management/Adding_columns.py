import pandas as pd
import os

file_path = '../TXT/MT4/BTCUSD5.csv'

df = pd.read_csv(file_path, parse_dates=[0])

insert_column_names = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
df.columns = insert_column_names
df['Time'] = pd.to_datetime(df['Time'], format='mixed')
df['Time'] = df['Time'].dt.strftime('%H:%M:%S')
file_name = os.path.basename(file_path)
df = df.assign(Filename=file_name)

print(df)


on_off = True      # turn on and off
if on_off:
    df.to_csv(file_path, index=False)
else:
    pass


