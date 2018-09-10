# Python file

# Import pandas
# from reader import login, checkEmail, checkPassword
import sys
sys.path.append('/')
import reader

# Developer Space
print()
print()
print()
print('Developer')

email = 'nraptor12345@gmail.com'
password = 'Dog1'
print(checkEmail('bob@gmail.com'))
print(checkEmail('steve@gmail.com'))
print("Email:", checkEmail(email))
print("Password:", checkPassword(email, 'pe'))
print("Password:", checkPassword(email, 'Dog1'))

print()
print("Login:", login(email, password))
