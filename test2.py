import numpy as np
import pandas as pd

# Sample DataFrame with additional columns
columns = ['Datetime',  'Open',  'High',  'Low',  'Close',  1,  2,  3]

data = [
    ['2024.04.13 23:53', 64811.90, 64873.59, 61083.99, 62152.97,  None,  None,  None],
    ['2024.04.13 23:54', 64811.90, 64873.59, 61083.99, 62152.97,  None,  None,  None],
    ['2024.04.14 00:00', 62156.57, 62875.54, 61434.34, 61861.70,  None,  None,  None],
    ['2024.04.14 00:30', 61877.27, 62723.31, 61711.07, 61813.97,  None,  None,  None],
    ['2024.04.14 01:00', 61810.49, 62967.39, 61783.92, 62948.15,  None,  None,  None],
    ['2024.04.14 01:30', 62948.94, 62948.94, 62138.76, 62805.36,  None,  None,  None],
    ['2024.04.14 02:00', 62805.54, 64627.23, 62786.02, 64316.13,  None,  None,  None],
    ['2024.04.14 02:30', 64315.27, 65613.49, 64193.24, 64430.19,  None,  None,  None],
    ['2024.04.14 03:00', 64433.12, 64715.16, 63723.79, 63816.65,  None,  None,  None],
    ['2024.04.14 03:30', 63953.17, 64332.17, 62913.37, 63574.05,  None,  None,  None],
    ['2024.04.14 04:00', 63582.40, 64290.27, 63516.58, 63692.66,  None,  None,  None],
    ['2024.04.14 04:35', 63692.75, 63933.52, 63280.98, 63814.64,  None,  None,  None],
    ['2024.04.14 05:00', 63960.39, 64008.89, 63685.80, 63769.89,  None,  None,  None],
    ['2024.04.14 05:30', 63769.65, 63981.45, 63335.20, 63522.86,  None,  None,  None],
    ['2024.04.14 06:00', 63523.04, 63548.01, 63026.67, 63092.29,  None,  None,  None],
    ['2024.04.14 06:30', 63092.21, 63163.61, 62142.07, 62737.97,  None,  None,  None],
    ['2024.04.14 07:00', 62736.91, 63581.41, 62695.44, 63447.30,  None,  None,  None],
    ['2024.04.14 07:30', 63446.89, 64184.05, 63402.32, 64158.92,  None,  None,  None],
    ['2024.04.14 08:00', 64153.78, 64153.78, 63830.70, 63969.45,  None,  None,  None],
    ['2024.04.14 08:30', 63969.46, 64418.88, 63934.68, 64277.14,  None,  None,  None],
    ['2024.04.14 09:00', 64277.16, 64474.21, 64164.52, 64399.60,  None,  None,  None],
    ['2024.04.14 09:30', 64399.60, 64682.56, 64122.55, 64676.90,  None,  None,  None],
    ['2024.04.14 10:00', 64676.90, 64894.33, 64521.37, 64669.32,  None,  None,  None],
    ['2024.04.14 10:30', 64669.31, 64860.76, 64538.46, 64594.68,  None,  None,  None],
    ['2024.04.14 11:00', 64594.68, 64751.08, 64268.12, 64475.72,  None,  None,  None],
    ['2024.04.14 11:30', 64475.75, 64865.35, 64381.45, 64856.07,  None,  None,  None],
    ['2024.04.14 12:00', 64855.79, 64888.75, 64430.84, 64546.78,  None,  None,  None],
    ['2024.04.14 12:30', 64544.08, 64737.64, 64218.40, 64355.04,  None,  None,  None],
    ['2024.04.14 13:00', 64355.68, 64468.60, 63931.69, 64147.68,  None,  None,  None],
    ['2024.04.14 13:30', 64147.68, 64357.91, 64147.29, 64304.70,  None,  None,  None],
    ['2024.04.14 14:00', 64305.02, 64668.13, 64304.04, 64465.18,  None,  None,  None],
]
dataframe = pd.DataFrame(data, columns=columns)
dataframe['Datetime'] = pd.to_datetime(dataframe['Datetime'])


# Function to find levels
def find_levels(filtered_df):
    sr_levels = []

    # Support and Resistance levels
    for i in range(2, len(filtered_df) - 2):
        if (filtered_df['Low'][i] < filtered_df['Low'][i - 1]) and \
                (filtered_df['Low'][i] < filtered_df['Low'][i + 1]) and \
                (filtered_df['Low'][i + 1] < filtered_df['Low'][i + 2]) and \
                (filtered_df['Low'][i - 1] < filtered_df['Low'][i - 2]):
            price_level_1 = filtered_df['Low'][i]
            if not is_near_level(price_level_1, sr_levels, filtered_df):
                sr_levels.append((i, price_level_1))  # SR levels

        elif ((filtered_df['High'][i] > filtered_df['High'][i - 1]) and
              (filtered_df['High'][i] > filtered_df['High'][i + 1]) and
              (filtered_df['High'][i + 1] > filtered_df['High'][i + 2]) and
              (filtered_df['High'][i - 1] > filtered_df['High'][i - 2])):
            price_level_1 = filtered_df['High'][i]
            if not is_near_level(price_level_1, sr_levels, filtered_df):
                sr_levels.append((i, price_level_1))  # SR levels

    return sr_levels


# Function to check if a level is near
def is_near_level(value, levels, df):
    average = np.mean(df['High'] - df['Low'])
    return any(abs(value - level[1]) < average for level in levels)


sr_levels_out = find_levels(dataframe)     # Function call

print('SR_levels_out: \n', sr_levels_out)
print('444', len(sr_levels_out))


def add_levels_columns_to_dataframe():
    # Initialize counters for columns for 5 levels as a dictionary
    n = 1
    column_counters = {}
    while n < (len(sr_levels_out) + 1):
        column_counters[n] = 0
        n += 1
    print(column_counters)

    # Loop through the price levels
    for idx, price in sr_levels_out:
        # Determine which column to assign the price level to
        column_number = min(column_counters, key=column_counters.get)
        # Update the DataFrame with the price level
        dataframe.loc[idx, column_number] = price
        # Increment the counter for the assigned column
        column_counters[column_number] += 1

    return column_counters


column_counters_outside = add_levels_columns_to_dataframe()


def fill_column_with_first_non_null_value(df, column_inx):
    # Check if any non-null value exists in the column
    if not df[column_inx].isna().all():
        # Get the first non-null value
        value_to_fill = df[column_inx].dropna().iloc[0]

        # Find the index of the first occurrence of the non-null value
        start_index = df.loc[df[column_inx] == value_to_fill].index[0]

        # Iterate through the DataFrame and fill the values with the non-null value
        for idx, val in df.iterrows():
            if idx >= start_index:
                df.loc[idx, column_inx] = value_to_fill


# Fill each column with the first non-null value
for column_index in range(1, len(column_counters_outside) + 1):
    fill_column_with_first_non_null_value(dataframe, column_index)

dataframe.set_index('Datetime', inplace=True)
print(dataframe)


def level_rejection_signals(df, sr_levels):
    rejection_signals = []
    df.reset_index(inplace=True)

    signal = None

    for index, row in df.iterrows():
        previous_close = df.iloc[index - 1]['Close']
        current_candle_close = row['Close']
        current_candle_high = row['High']
        current_candle_low = row['Low']

        for level_column in range(1, 4):
            current_sr_level = row[level_column]
            if current_sr_level is not None:
                if previous_close < current_sr_level:  # Check if the previous close was below the resistance level
                    if current_candle_high > current_sr_level:  # Price has crossed above resistance level
                        if current_candle_close < current_sr_level:  # but closed below
                            signal = -100

                            break

                elif previous_close > current_sr_level:  # Check if the previous close was above the support level
                    if current_candle_low < current_sr_level:  # Price has crossed below support level
                        if current_candle_close > current_sr_level:  # but closed above
                            signal = 100

                            break
        else:
            rejection_signals.append(None)
    rejection_signals.append(signal)

    print('Rejection_signals: ', rejection_signals)
    rejection_signals_series = pd.Series(rejection_signals)
    return rejection_signals_series


rejection_signals_series_outside = level_rejection_signals(dataframe, sr_levels_out)
print(rejection_signals_series_outside)