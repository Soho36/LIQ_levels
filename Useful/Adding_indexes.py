# adding indexes to CSV
import pandas as pd

df = pd.read_csv('Ta-lib patterns.csv')

df.to_csv('Ta-lib patterns.csv', index=True)

print(df)