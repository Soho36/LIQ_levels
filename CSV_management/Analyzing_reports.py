import pandas as pd

file_path_source = 'E:/YandexDisk/Desktop_Zal/AUDNZD_report/audnzd_grid_ticked.csv'
file_path_result = 'E:/YandexDisk/Desktop_Zal/AUDNZD_report/audnzd_grid_result_monthly.csv'
columns_to_parse = ['Date', 'Profit', 'Balance']
df = pd.read_csv(file_path_source, parse_dates=[0], sep=',', usecols=columns_to_parse)
print('\nSource DF: \n', df.head())

df['Date'] = pd.to_datetime(df['Date'])

df['Time'] = df['Date'].dt.time
df['Date'] = df['Date'].dt.date

print('\nSplitted time and date: \n', df.head())

column_sum = df['Profit'].sum()
print('\nAlltime profit: ', round(column_sum, 2))

df['Date'] = pd.to_datetime(df['Date'])
monthly_profits = df.groupby(df['Date'].dt.to_period('M'))['Profit'].sum()
print('Monthly profits: \n', monthly_profits)

on_off = True
if on_off:
    monthly_profits.to_csv(file_path_result, index=True)

