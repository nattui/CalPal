# Python module checks if the pass user information matches with the database

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

# Create users: If email is unique, add user to the database
def userCreation(fname, lname, email, password):
  if checkEmail(email):
    return False
  else:
    list_fname.append(fname)
    list_lname.append(lname)
    list_email.append(email)
    list_password.append(password)

    # Create a Pandas dataframe from the data.
    df = pd.DataFrame({'First Name': list_fname, 'Last Name': list_lname,
                       'Email': list_email, 'Password': list_password})

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('../database/database.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    return True


def refreshDatabase():
  # Create a Pandas dataframe from the excel file
  df = pd.read_excel('../database/database.xlsx', sheet_name='Sheet1')

  # Save columns as list
  list_fname = convert(df['First Name'])
  list_lname = convert(df['Last Name'])
  list_email = convert(df['Email'])
  list_password = convert(df['Password'])

  # Create a dictionary (KEY email: VALUE password) for user information
  dict_email_password = {}
  for i in range(len(list_email)):
    dict_email_password[list_email[i]] = list_password[i]

def getDatabase():
  list = []
  list.append(list_fname)
  list.append(list_lname)
  list.append(list_email)
  list.append(list_password)
  return(list)

# Create a Pandas dataframe from the excel file
df = pd.read_excel('../database/database.xlsx', sheet_name='Sheet1')

# Save columns as list
list_fname = convert(df['First Name'])
list_lname = convert(df['Last Name'])
list_email = convert(df['Email'])
list_password = convert(df['Password'])

# Create a dictionary (KEY email: VALUE password) for user information
dict_email_password = {}
for i in range(len(list_email)):
  dict_email_password[list_email[i]] = list_password[i]


if __name__ == '__main__':
  print()

  print("BEFORE:", list_email)

  fname = 'Jasmine'
  lname = 'Mai'
  email = 'jasmine@gmail.com'
  password = 'Cat2'

  print("USER CREATED:", userCreation(fname, lname, email, password))
  print("AFTER:", list_email)

  print("DONE")
