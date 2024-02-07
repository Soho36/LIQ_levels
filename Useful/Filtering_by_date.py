import pandas as pd

df = pd.read_csv('TXT/MT4/BTCUSD_m5.csv', parse_dates=[0])
print(df.head())

start_date = '2023-06-23'
end_date = '2023-06-24'

# start_date = pd.to_datetime(start_date)
# end_date = pd.to_datetime(end_date)
# print(start_date)
# print(end_date)

date_range = pd.date_range(start=start_date, end=end_date, freq='D')
print('Date range: ', list(date_range))

date_column = df['Date']
dates_in_range = date_column.isin(date_range)

df_filtered_by_date = df[dates_in_range]
print('df_filtered_by_date: ', df_filtered_by_date)

