import pandas as pd
import os

MT4_format = False  # False for MT5 format
MT5_daily = False    # If MT5 csv is daily
file_path = '../History_data/MT5/TSLA_M5.csv'

df = pd.read_csv(file_path, parse_dates=[0], delimiter='\t')  # Tab is default delimiter for MT5 files

if MT4_format:  # Insert column names if MT4 format
    insert_column_names = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df.columns = insert_column_names
    df['Time'] = pd.to_datetime(df['Time'], format='mixed')
    df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

elif MT5_daily:
    new_column_names = {'<DATE>': 'Date',
                        '<OPEN>': 'Open', '<HIGH>': 'High', '<LOW>': 'Low', '<CLOSE>': 'Close', '<VOL>': 'Volume'}
    df = df.rename(columns=new_column_names)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = '00:00:00'

else:   # Rename column names if MT5 format
    new_column_names = {'<DATE>': 'Date', '<TIME>': 'Time',
                        '<OPEN>': 'Open', '<HIGH>': 'High', '<LOW>': 'Low', '<CLOSE>': 'Close', '<TICKVOL>': 'Volume'}
    df = df.rename(columns=new_column_names)
    df['Time'] = pd.to_datetime(df['Time'], format='mixed')
    df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

file_name = os.path.basename(file_path)
df = df.assign(Filename=file_name)

print(df)


on_off = True      # turn on and off
if on_off:
    df.to_csv(file_path, index=False, sep=',')
else:
    pass


