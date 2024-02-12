import pandas as pd

# Sample DataFrame with 'Date' and 'Time' columns
data = {'Date': ['2023-06-23', '2023-06-24', '2023-06-25'],
        'Time': ['00:00:00', '12:00:00', '23:59:59']}
df = pd.DataFrame(data)

# Concatenate 'Date' and 'Time' columns into a single string
datetime_str = df['Date'] + ' ' + df['Time']

# Convert the concatenated string to datetime format and assign it to a new column 'Datetime'
df['Datetime'] = pd.to_datetime(datetime_str)

first_row = df.iloc[1]
print(first_row)

# Display the DataFrame with the new 'Datetime' column
print(df)