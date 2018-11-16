
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 15.11.2018

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
  return email in list_email


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
  
  # BUG: becomes apparent here!
  # ~ print(email, email_list)
  
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
  
  # Retreives all relevant columns user data. 
  first_name_data   = datafile["First Name"]
  last_name_data    = datafile["Last Name"]
  gender_data       = datafile["Gender"]
  birth_day_data    = datafile["Birth-day"]
  birth_month_data  = datafile["Birth-month"]
  birth_year_data   = datafile["Birth-year"]
  height_data       = datafile["Height"]
  weight_data       = datafile["Weight"]
  calorie_goal_data = datafile["Calorie goal"]
  
  # Retrieves the index associated with the user's email. 
  index = datafile.loc[datafile["Email"] == email].index[0]
  
  # Generates a list of all relevant user data using the data columns
  # and the user's index. 
  user_data = []
  
  for data_list in (first_name_data, 
                    last_name_data, 
                    gender_data, 
                    birth_day_data, 
                    birth_month_data, 
                    birth_year_data, 
                    height_data, 
                    weight_data, 
                    calorie_goal_data):
                    
    user_data.append(data_list[index])
  
  # Returns the user's data.
  return user_data


def createUser(fname, 
               lname, 
               email, 
               password, 
               gender, 
               birth_day, 
               birth_month, 
               birth_year, 
               height, 
               weight,
               calorie_goal):
  """
  Create users: If email is unique, add user to the database
  """
  
  # Checks if the email is in the database. 
  isEmailInDatabase = email in list_email
  
  # Only creates a new user if the email is not currently 
  # in the database. 
  if not isEmailInDatabase:
    
    # Uses a for loop to add each data field to 
    # their respective columns. 
    for data_list, new_data in ((list_fname,        fname), 
                                (list_lname,        lname), 
                                (list_email,        email), 
                                (list_password,     password), 
                                (list_gender,       gender), 
                                (list_birth_day,    birth_day), 
                                (list_birth_month,  birth_month), 
                                (list_birth_year,   birth_year), 
                                (list_height,       height), 
                                (list_weight,       weight), 
                                (list_calorie_goal, calorie_goal), ):
      data_list.append(new_data)
    
    # Adds the email and password to a dictionary. 
    dict_email_password[email] = password

    # Creates a Pandas dataframe from the data.
    df = pd.DataFrame({"First Name"   : list_fname, 
                       "Last Name"    : list_lname, 
                       "Email"        : list_email, 
                       "Password"     : list_password, 
                       "Gender"       : list_gender, 
                       "Birth-day"    : list_birth_day, 
                       "Birth-month"  : list_birth_month, 
                       "Birth-year"   : list_birth_year, 
                       "Height"       : list_height, 
                       "Weight"       : list_weight, 
                       "Calorie goal" : list_calorie_goal, })
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(getDatabasePath(), engine="xlsxwriter")

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def getDatabase():
  """
  Returns the entire user database, including all user names, emails
  passwords, and other information. 
  """
  
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
    
    # ~ createUser(fname, 
               # ~ lname, 
               # ~ email, 
               # ~ password, 
               # ~ gender, 
               # ~ birth_day, 
               # ~ birth_month, 
               # ~ birth_year, 
               # ~ height)
    
