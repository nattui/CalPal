
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 05.11.2018

reader.py
A Python module checks if the pass user information 
matches with the database.

TODO: Optimize the reading and writing database
"""

# Import pandas
import pandas as pd
import timeit

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


def checkLogin(email, password):
  """
  Validates the user email and password.

  Args:
      email (str): The email from the submitted form.
      password (str): The password from the submitted form.

  Returns:
      bool: True when the email and password matches the database, False otherwise.
  """
  
  # Checks if email is in email database
  if (email in df['Email'].values):
  
    # Checks if email and password matches the database
    index = df.loc[df['Email'] == email].index[0]
    
    if ((df['Email'][index] == email) and (df['Password'][index] == password)):
      return True
          
  return False


def returnFirstLastName(email):
  """
  A function that returns the first and last name of a user givern
  the user's email. This is specifically used in 
  login_redirect. 
  
  Returns an array of two strings:
    ("first_name", "last_name")
  """
  
  # Retreives all the first and last names. 
  first_name_data = df["First Name"]
  last_name_data = df["Last Name"]
  
  # Retrieves the index associated with the user's email. 
  index = df.loc[df['Email'] == email].index[0]
  
  # Retrieves the first and last name using the index. 
  first_name = first_name_data[index]
  last_name = last_name_data[index]
  
  # Returns the first and last names. 
  return (first_name, last_name)


# Create users: If email is unique, add user to the database
def userCreation(fname, lname, email, password):
  if checkEmail(email):
      return False
  else:
    list_fname.append(fname)
    list_lname.append(lname)
    list_email.append(email)
    list_password.append(password)
    dict_email_password[email] = password

    # Create a Pandas dataframe from the data.
    df = pd.DataFrame({'First Name': list_fname, 'Last Name': list_lname, 'Email': list_email, 'Password': list_password})
    
    # Changes the path of the database depending on whether or not the
    # function is run on reader.py or app.py. 
    if __name__ == "__main__":
      database_path = "../../database/database.xlsx"
    else:
      database_path = "../database/database.xlsx"
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(database_path, engine="xlsxwriter")

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    return True


def getDatabase():
  list = []
  list.append(list_fname)
  list.append(list_lname)
  list.append(list_email)
  list.append(list_password)
  return(list)

start = timeit.default_timer()

# Changes path of the database depending on whether or not the
# function is run on reader.py or app.py. 
if __name__ == "__main__":
  database_path = "../../database/database.xlsx"
else:
  database_path = "../database/database.xlsx"

# Create a Pandas dataframe from the excel file
df = pd.read_excel(database_path, sheet_name="Sheet1")

# Save columns as list
list_fname = convert(df['First Name'])
list_lname = convert(df['Last Name'])
list_email = convert(df['Email'])
list_password = convert(df['Password'])

stop = timeit.default_timer()
print()
print('Time: ', stop - start)
print()

# Create a dictionary (KEY email: VALUE password) for user information
dict_email_password = {}
for i in range(len(list_email)):
    dict_email_password[list_email[i]] = list_password[i]
# print("EMAL PASSWORD")

if __name__ == '__main__':
    # ~ print()
    # ~ print("BEFORE:", list_email)

    fname = 'Jasmine'
    lname = 'Mai'
    email = 'jasmine@gmail.com'
    password = 'Cat2'
    
    print(returnFirstLastName(email))
    
    # ~ print("USER CREATED:", userCreation(fname, lname, email, password))
    # ~ print("AFTER:", list_email)

    # ~ print("DONE")
