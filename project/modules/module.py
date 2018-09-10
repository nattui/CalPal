# Developer Space for Python code

from reader import checkLogin, checkEmail, checkPassword

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
print("Login:", checkLogin(email, password))
