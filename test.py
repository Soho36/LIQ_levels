import pandas as pd

filepath = 'tc2000.txt'
df = pd.read_csv(filepath, parse_dates=[0], dayfirst=True)

print(df)


