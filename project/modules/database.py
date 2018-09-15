# Import pandas
import pandas as pd

# Create a Pandas dataframe from the excel file
df = pd.read_excel('../../database/database.xlsx', sheet_name='Sheet1')

print(df)
print()
print(df['First Name'])

print(df['Last Name'])
print(df['Email'])
print(df['Password'])

print()

print(df.columns)
print(df.index)

print()
# First Name
print('COLUMN:', df.columns[0])
print('TYPE:', type(df.columns[0]))
print('First Name' == df.columns[0])


print()
# Prints the columns
for i in df.columns:
    print(i)

print()
print()

# Print John
# print("NAME", df['First Name'][0])

print()
# print(df['Email'] == 'tim@apple.com')
print()
# print(df['Email'].index('tim@apple.com'))
print("DEBUG:", df['Email'].index)

print()
print('INDEX:', df.loc[df['Email'] == 'tim@apple.com'].index[0])
# print('INDEX:', df.loc[df['Email'] == 'jasmine@apple.com'].index[0])
print()
# Checks if email is in email values
print('tim@apple.com' in df['Email'].values)

print()
# print(df[''])

def checkLogin(email, password):
    '''
    Validates the user email and password.

    Args:
        email (str): The email from the submitted form.
        password (str): The password from the submitted form.

    Returns:
        bool: True when the email and password matches the database, False otherwise.
    '''

    # Checks if email is in email database
    if (email in df['Email'].values):
        # Checks if email and password matches the database 
        if ((df.loc[df['Email'] == email].index[0]) == (df.loc[df['Password'] == password].index[0])):
            return True;
    return False;

def userInformation(email):
    '''
    Gets the user information in a dictionary.

    Args:
        email (str): The email from the submitted form.

    Returns:
        dict: User information such as First and Last Name and email.
    '''
    
    userInformation = {}
    userInformation['First Name'] = df['First Name'][df.loc[df['Email'] == email].index[0]]
    userInformation['Last Name'] = df['Last Name'][df.loc[df['Email'] == email].index[0]]
    userInformation['Email'] = email
    return userInformation
    

print('Login Validation:', checkLogin('tim@apple.com', 'apple'))
print('Login Validation:', checkLogin('tim@apple.comm', 'apple'))
print('Login Validation:', checkLogin('tim@apple.com', '123'))

userInformation('tim@apple.com')

pizza = {}
pizza['apple'] = 'apple1'
print(type(pizza))
