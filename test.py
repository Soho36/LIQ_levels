import pandas as pd

file_path = 'Bars/MESU24_M1_w.csv'

start_date = '2024-06-17'       # Choose the start date to begin from
end_date = '2024-06-19'         # Choose the end date


def getting_dataframe_from_file(path):
    columns_to_parse = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    csv_df = pd.read_csv(
        path,
        parse_dates=[0],
        dayfirst=False,
        usecols=columns_to_parse
    )

    print()
    return csv_df


dataframe_from_csv = getting_dataframe_from_file(file_path)
print(dataframe_from_csv)


def date_range_func(df_csv, start, end):

    date_range = pd.date_range(
        start=start,
        end=end,
        freq='D'
    )

    df = df_csv

    date_column = df['Date']        # Select the 'Date' column from the DataFrame
    dates_in_range = date_column.isin(date_range)   # checks which dates from date_column fall within the generated
    # date range, resulting in a boolean mask
    df_filtered_by_date = df[dates_in_range]

    if df_filtered_by_date.empty:
        print('NB! Dataframe is empty, check the date range!')
        exit()  # If dataframe is empty, stop the script

    else:
        return df_filtered_by_date


filtered_by_date_dataframe = date_range_func(dataframe_from_csv, start_date, end_date)
print(filtered_by_date_dataframe)

filtered_by_date_dataframe_datetime = (
    filtered_by_date_dataframe.assign(
        Datetime=(filtered_by_date_dataframe['Date'] + pd.to_timedelta(filtered_by_date_dataframe['Time'])))
)
print(filtered_by_date_dataframe_datetime)
print()

filtered_by_date_dataframe_datetime.set_index('Date', inplace=True)
print(filtered_by_date_dataframe_datetime)


df_h1 = filtered_by_date_dataframe_datetime.resample('H').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last'
})

print(df_h1)
