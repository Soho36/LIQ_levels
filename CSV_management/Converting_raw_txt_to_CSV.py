import pandas as pd

# Read the text file
with open('Ta-lib patterns.txt', 'r') as file:
    lines = file.readlines()

print(lines)
# # Split each line into columns using whitespace
data = [line.strip().split() for line in lines]
#
print('List of lines: ', data)
print()
pattern_code_list = []
pattern_name_list = []

for i in data:
    pattern_code_list.append(i[0])
    pattern_name_list.append(i[1::])

print('List of pattern codes: ', pattern_code_list)

pattern_names = []
for i in pattern_name_list:
    joined = ' '.join(i)
    pattern_names.append(joined)
print('List of pattern names:', pattern_names)
#
# # # Create a DataFrame
df = pd.DataFrame({'PatternCode': pattern_code_list, 'PatternName': pattern_names})
print(df)

# # Save to CSV
df.to_csv('Ta-lib patterns.csv', index=False)