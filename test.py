import pandas as pd


df = pd.read_csv('Ta-lib patterns.csv')

pattern_code = df['PatternCode'].iloc[1]

df.to_csv('Ta-lib patterns.csv', index=True)

print(df)
print(pattern_code)