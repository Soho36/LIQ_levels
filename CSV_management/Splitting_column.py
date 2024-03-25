import pandas as pd
pd.set_option('display.max_columns', 10)

# READING FILE

filepath = '../TXT/STOCKS/meta_D1.csv'
df = pd.read_csv(filepath, parse_dates=[0], dayfirst=True)
print('Source dataframe: '.upper())
print(df)

# CONVERTING TO DATETIME
df['Date'] = pd.to_datetime(df['Date'])

# ADDING TIME COLUMN
df['Time'] = df['Date'].dt.strftime('%H:%M:%S')
print('1.dt.time\n', df.head())

# ADDING DATE COLUMN
df['Date'] = df['Date'].dt.date
print('2.dt.date\n', df.head())


# WRITING FILE
on_off = True
if on_off:
    df.to_csv(filepath, index=False)
else:
    pass
