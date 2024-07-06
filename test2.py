import pandas as pd

file_path = 'Bars/MESU24_M1_w.csv'

start_date = '2024-06-17'
end_date = '2024-06-19'


def getting_dataframe_from_file(path):
    columns_to_parse = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    csv_df = pd.read_csv(
        path,
        usecols=columns_to_parse
    )
    return csv_df


dataframe_from_csv = getting_dataframe_from_file(file_path)
print(dataframe_from_csv)


def date_range_func(df_csv, start, end):
    # Combine 'Date' and 'Time' into 'DateTime' and convert to datetime
    df_csv['DateTime'] = pd.to_datetime(df_csv['Date'] + ' ' + df_csv['Time'])
    df_filtered_by_date = df_csv[(df_csv['DateTime'] >= start) & (df_csv['DateTime'] <= end)]
    if df_filtered_by_date.empty:
        print('NB! Dataframe is empty, check the date range!')
        exit()
    else:
        return df_filtered_by_date


filtered_by_date_dataframe = date_range_func(dataframe_from_csv, start_date, end_date)
print(filtered_by_date_dataframe)

# Set the combined datetime column as the index
filtered_by_date_dataframe.set_index('DateTime', inplace=True)
print(filtered_by_date_dataframe)

# Resample 1-minute data to 1-hour data
df_h1 = filtered_by_date_dataframe.resample('H').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last'
})

print(df_h1)
