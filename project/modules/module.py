# Python file

# Import pandas
import pandas as pd

# Assign spreadsheet to file
file = '../../database/database.xlsx'

# Load spreadsheet
xl = pd.ExcelFile(file)

# Print the sheet names
# print(xl.sheet_names)

# Load a sheet into a DataFrame by name
df = xl.parse('Sheet1')

# print(type(df))

print()
print()
print()

print(df)
print()

print(df['First Name'][1])
print()

list_email = df['Email']

# Prints all the elements in the column
for i in df.index:
  print(df['Email'][i])

print()

for i in list_email:
  print('Email:', i)
