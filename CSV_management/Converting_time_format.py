import pandas as pd

# READING
df = pd.read_csv('../TXT/MT4/BTCUSD_m60.csv', parse_dates=[0])
print(df.head())

# Convert 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time'])
# Format 'Time' column to include seconds
df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

print(df.head())

# WRITING
on_off = False      # turn on and off
if on_off:
    df.to_csv('../TXT/MT4/BTCUSD_m60.csv', index=False)
else:
    pass

# df['Time'].dt.strftime('%H:%M:%S'): Accesses the datetime properties of the 'Time' column and applies the strftime
# method to format the time values.
# df['Date'].dt.day: Accesses the day component of the datetime objects in the 'Date' column.
# df['Datetime'].dt.hour: Accesses the hour component of the datetime objects in the 'Datetime' column.

