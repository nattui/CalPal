#!/usr/bin/python3
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 20.11.2018

reader.py
A Python module checks if the pass user information 
matches with the database.

TODO: Optimize the reading and writing database
"""

# Import pandas
import pandas as pd
import timeit


def convert(df_column):
  """
  Converts a DataFrame column to list
  """
  data_list = []
  
  for element in df_column:
      data_list.append(element)
      
  return data_list


def checkEmail(email):
  """
  Checks if a given email is currently in the database. 
  """
  email_list = getDatabase()[2]
  
  return email in email_list


def checkLogin(email, password):
  """
  Validates the user email and password.

  Args:
      email (str): The email from the submitted form.
      password (str): The password from the submitted form.

  Returns:
      bool: True when the email and password matches the database, False otherwise.
  """
  
  # Retrieves the entire user database. 
  database = getDatabase()
  
  # Retrieves the list of emilas and passwords. 
  email_list = database[2]
  password_list = database[3]
  
  # Checks if the inputted email exists in the database. 
  if email in email_list:
    
    # Gets the index associated with the row of the user's data. 
    user_index = email_list.index(email)
    
    # Returns True if the inputted email and password match
    if email_list[user_index] == email and password_list[user_index] == password:
      return True
  
  # Returns False if the email is not in the database. 
  else:
    return False


def getUserData(email):
  """
  A function that returns a user's data given the user's email. 
  This is specifically used in login_redirect. 
  
  Returns a list of strings
  """
  
  # Retrieves the datafile. 
  datafile = pd.read_excel(getDatabasePath(), sheet_name="Sheet1")
  
  # Retrieves the index associated with the user's email. 
  index = datafile.loc[datafile["Email"] == email].index[0]
  
  # A list that will eventually store all of ther user's data. 
  user_data = []
  
  # Iterates though ever list in the database. 
  for data_list in getDatabase():

    # When integers are read, they're actually read as int64 types.
    # This converts them to conventional ints.  
    try:
      add_data = int(data_list[index])
    except ValueError:
      add_data = data_list[index]
    
    # Adds the piece of data to user_data. 
    user_data.append(add_data)
  
  # Returns the user's data.
  return user_data


def createUser(new_user_data):
  """
  Creates a new users if the inputted email is unique.
  
  new_user_data is formatted:
    [fname, 
     lname, 
     email, 
     password, 
     gender, 
     birth_day, 
     birth_month, 
     birth_year, 
     height, weight, 
     calorie_goal]
  """
  
  # Retrieves the inputted email. 
  email = new_user_data[2]
  
  # Only creates a new user if the email is not currently 
  # in the database. 
  if not checkEmail(email):
    
    # Adds the email and password to a dictionary.
    password = new_user_data[3] 
    dict_email_password[email] = password

    # A list that will eventually become the new database. 
    new_database = []
    
    # Iterates through every column in the database. 
    for index, column in enumerate(getDatabase()):
      
      # Appends the new user data to the column.
      column.append(new_user_data[index])
      
      # Appends the column, now with the new user data added, to
      # the new database. 
      new_database.append(column)
    
    # Writes the new database to database.xlsx
    writeToDatabase(new_database)


def writeNewUserData(old_email, new_user_data):
  """
  Writes a set of new user data to database.xlsx. 
  """
  # Retrieves the datafile. 
  datafile = pd.read_excel(getDatabasePath(), sheet_name="Sheet1")

  # Retrieves the index associated with the user's previous email. 
  user_index = datafile.loc[datafile["Email"] == old_email].index[0]
  
  # A list that will eventually store the updated user batabase. 
  updated_database = []
  
  # Iterates through every column in the database. 
  for data_index, column in enumerate(getDatabase()):
    
    # Replaces the value in the column at the given user's index
    # with the new user data. 
    column[user_index] = new_user_data[data_index]
    
    # Adds the column to the updated database. 
    updated_database.append(column)
    
  # Writes the updated database to database.xlsx. 
  writeToDatabase(updated_database)

  

def getDatabase():
  """
  Returns the entire user database, including all user names, emails
  passwords, and other information. 
  """
  
  # Create a Pandas dataframe from the excel file
  df = pd.read_excel(getDatabasePath(), sheet_name="Sheet1")
  
  # A list that will store all the values in the database.
  # This will be the final output. 
  database = []
  
  # Uses a for loop to iterate each column of the database. 
  for column_name in ("First Name", 
                      "Last Name", 
                      "Email", 
                      "Password", 
                      "Gender", 
                      "Birth-day", 
                      "Birth-month", 
                      "Birth-year", 
                      "Height", 
                      "Weight", 
                      "Calorie goal"):
    
    # Retrieves the database column. 
    database_column = convert(df[column_name])
    
    # Appends the solumn to the final output. 
    database.append(database_column)
  
  # Returns the final output. 
  return database
  

def writeToDatabase(new_database):
  """
  Takes a list of columns and writes the columns to database.xlsx
  
  This function is used in both createUser and writeNewUserData. 
  """
  
  # A dictionary that will store the column names as keys
  # and a list of data as values. 
  dataframe_dict = {}
  
  # Uses a for loop to interate through each column name
  for column_index, column_name in enumerate(("First Name", 
                                              "Last Name", 
                                              "Email", 
                                              "Password", 
                                              "Gender", 
                                              "Birth-day", 
                                              "Birth-month", 
                                              "Birth-year", 
                                              "Height", 
                                              "Weight", 
                                              "Calorie goal")):
    
    # Assigns the column name to the list in the new database. 
    dataframe_dict[column_name] = new_database[column_index]
  
    # Creates a Pandas dataframe from the data.
    df = pd.DataFrame(dataframe_dict)
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(getDatabasePath(), engine="xlsxwriter")

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def getDatabasePath():
  """
  Returns the path of the database depending on whether or not this
  file is being run on reader.py or app.py. 
  """
  
  if __name__ == "__main__":
    database_path = "../../database/database.xlsx"
  else:
    database_path = "../database/database.xlsx"
    
  return database_path
  

#=======================================================================


# Create a Pandas dataframe from the excel file
df = pd.read_excel(getDatabasePath(), sheet_name="Sheet1")

# Save columns as list
list_fname        = convert(df["First Name"])
list_lname        = convert(df["Last Name"])
list_email        = convert(df["Email"])
list_password     = convert(df["Password"])
list_gender       = convert(df["Gender"])
list_birth_day    = convert(df["Birth-day"])
list_birth_month  = convert(df["Birth-month"])
list_birth_year   = convert(df["Birth-year"])
list_height       = convert(df["Height"])
list_weight       = convert(df["Weight"])
list_calorie_goal = convert(df["Calorie goal"])

# Create a dictionary (KEY email: VALUE password) for user information
dict_email_password = {}
for i in range(len(list_email)):
    dict_email_password[list_email[i]] = list_password[i]


if __name__ == "__main__":

    fname = "John"
    lname = "Doe"
    email = "john.doe@gmail.com"
    password = "testing"
    gender = "Female"
    birth_day = 1
    birth_month = 12
    birth_year = 1998
    height = 70

    print(getUserData("stan.smith@gmail.com"))
    
    
