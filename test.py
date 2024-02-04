import pandas as pd

# Create a DataFrame from a dictionary
data = {'Name': ['John', 'Alice', 'Bob'],
        'Age': [25, 28, 22],
        'City': ['New York', 'San Francisco', 'Los Angeles']}

df = pd.DataFrame(data)

# Print the DataFrame
print(df)
