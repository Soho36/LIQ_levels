import pandas as pd
import os

file_path = '../TXT/MT4/BTCUSD1.csv'

df = pd.read_csv(file_path, parse_dates=[0])


file_name = os.path.basename(file_path)
insert_column_names = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Filename']
df.columns = insert_column_names
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')
df['Time'] = df['Time'].dt.strftime('%H:%M:%S')
print(df)


on_off = False      # turn on and off
if on_off:
    df.to_csv(file_path, index=False)
else:
    pass


