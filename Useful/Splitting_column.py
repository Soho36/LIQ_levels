import pandas as pd
pd.set_option('display.max_columns', 10)

# READING FILE

filepath = '../TXT/tsla_D1.csv'
df = pd.read_csv(filepath, parse_dates=[0], dayfirst=True)

df['Date'] = pd.to_datetime(df['Date'])
print(df.head())

df['Time'] = df['Date'].dt.strftime('%H:%M:%S')
print('1.dt.time\n', df.head())

df['Date'] = df['Date'].dt.date
print('2.dt.date\n', df.head())


# WRITING FILE
on_off = True
if on_off:
    df.to_csv(filepath, index=False)
else:
    pass
