# Module for reading Python files

# Import pandas
import pandas as pd

# Convert DataFrame column to list
def convert(df_column):
  list = []
  for element in df_column:
    list.append(element)
  return list

# Checks if the email exist in the database
def checkEmail(email):
  if email in list_email:
    return(True)
  else:
    return(False)

# Checks if the email match the password
def checkPassword(email, password):
  if password == dict_email_password[email]:
    return(True)
  else:
    return(False)

# Checks form information with the database
def checkLogin(email, password):
  if checkEmail(email):
    return(checkPassword(email, password))
  else:
    return(False)


# Load a spreadsheet file into a DataFrame
# df = pd.read_excel('../../database/database.xlsx', sheet_name='Sheet1')
df = pd.read_excel('../database/database.xlsx', sheet_name='Sheet1')

# Save columns as list
list_fname = convert(df['First Name'])
list_lname = convert(df['Last Name'])
list_email = convert(df['Email'])
list_password = convert(df['Password'])

# Create a dictionary for user information
dict_email_password = {}

# Email as the key and password as the value
for i in range(len(list_email)):
  dict_email_password[list_email[i]] = list_password[i]

# Prints all of the email and password
for i in dict_email_password:
  print('Email:', i)
  print('Password:', dict_email_password[i])

