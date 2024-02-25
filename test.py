import pandas as pd
import talib

# Define a custom example dataframe
example_dataframe = pd.DataFrame({
    'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
    'High': [100, 110, 105, 115, 120],
    'Close': [95, 100, 100, 110, 105]
})

# Define other necessary variables (you need to define these according to your actual code)
sr_levels_timeframe = 5

# Call the function with the custom example dataframe
print(example_dataframe)


def level_peirce_recognition(example_df):

    swing_highs = talib.MAX(example_df['High'], sr_levels_timeframe)
    print(swing_highs)
    swing_highs.reset_index(drop=True, inplace=True)
    print('Swing highs length: ', len(swing_highs))
    signals = []
    if len(swing_highs) != len(example_df):
        print('Error lengths are not the same')
        return

    for i in range(1, len(example_df)):
        print(f"i: {i}, swing_highs[i-1]: {swing_highs[i - 1]}, filtered_by_date_dataframe['High'][i]: {example_df['High'][i]}")

        if i > 0 and example_df['High'][i] > swing_highs[i - 1]:

            if example_df['Close'][i] < swing_highs[i - 1]:
                signals.append('Signal generated')

    print(f'Level pierce signals: {signals}')


level_peirce_recognition(example_dataframe)