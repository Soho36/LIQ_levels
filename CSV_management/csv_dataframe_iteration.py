import pandas as pd

# Sample data for two DataFrames
data1 = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 22]}
data2 = {'Product': ['Laptop', 'Phone', 'Tablet'], 'Price': [1200, 800, 300]}

# Create two DataFrames
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

print(df1)
print(df2)

# Save DataFrames to CSV files
df1.to_csv('file1.csv', index=False)
df2.to_csv('file2.csv', index=False)

# List of CSV files
file_list = ['file1.csv', 'file2.csv']

# List of DataFrames
data_frames = [df1, df2]
#
# # Iterate over pairs of file and DataFrame, and save DataFrames to corresponding files
for file, df in zip(file_list, data_frames):
    df.to_csv(file, index=False)
#
# # Check the content of the updated CSV files
for file in file_list:
    print(f"Content of {file}:")
    print(pd.read_csv(file))
    print()
