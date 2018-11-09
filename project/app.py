
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 08.11.2018

This is where the python flask code occupies
TODO: Reseach G package
TODO: Finish the dashboard page

Note for later: For an unknown reason, the program returns an 
IndexingError when trying to login after the user has created an account. 
Still don't know why that is...
"""

from flask import (Flask, 
                   render_template, 
                   redirect, url_for, 
                   request, 
                   Blueprint, 
                   session)
from modules.reader import (checkLogin, 
                            checkEmail, 
                            getDatabase, 
                            getUserData,
                            createUser)

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

main = Blueprint("main", __name__)


# Redirects to the login page
@main.route("/")
def index():
    return redirect(url_for('main.login'))


# User login page
@main.route("/login")
def login():
    return render_template("login.html")


# Handles the login page logic
@main.route("/login", methods=["GET", "POST"])
def login_redirect():

    # Stores login user information 
    session["email"] = request.form["email"]
    session["password"] = request.form["password"]
    
    # Retrieves an array with two string values:
    #   ("first_name", "last_name")
    user_data = getUserData(session["email"])
    
    # Assigns the first and last names as attributes to session. 
    session["fname"] = user_data[0]
    session["lname"] = user_data[1]
    
    # If user information matches the information in the database, continue to application
    if checkLogin(session["email"], session["password"]):
        return redirect(url_for('main.dashboard'))
    else:
        return render_template("login.html", loginFailure=True)


# If the user is sucessfully created
@main.route("/login/success")
def signup_success():
    return render_template("login.html", userCreation=True)


# User signin page
@main.route("/signup")
def signup():
    return render_template("signup.html")


# Handles the sign up page logic
@main.route("/signup", methods=["GET", "POST"])
def signup_redirect():

    # Retrieves the user's height in feet and inches and converts 
    # them to integers.  
    height_feet   = int(request.form["height-feet"])
    height_inches = int(request.form["height-inches"])
    
    # Sums the total height in inches and converts it into a string. 
    total_height = str((height_feet * 12) + height_inches)
    
    # Uses a for loop to iterate through ever piece of user information.
    for var_name in ("fname", 
                     "lname", 
                     "email", 
                     "password", 
                     "gender", 
                     "birth-day", 
                     "birth-month", 
                     "birth-year", 
                     "height"):
      
      # For the case of birth month...
      if var_name == "birth-month":
      
        # Retrieves the name of the user's birth month. 
        month_name = request.form[var_name]
        
        # A dictionary that converts a month name to its
        # corresponding number. 
        month_name_to_number = \
          {"January"   : "1",
           "February"  : "2", 
           "March"     : "3",
           "April"     : "4", 
           "May"       : "5",
           "June"      : "6", 
           "July"      : "7",
           "August"    : "8", 
           "September" : "9",
           "October"   : "10", 
           "November"  : "11",  
           "December"  : "12", }
          
        # Converts the the user's birth month to its
        # corresponing number. 
        month_num = month_name_to_number[month_name]
        
        # Assigns the month number as an attribute. 
        session[var_name] = month_num
      
      # The assigned variable for height is different than other 
      # attributes because the total height was calculated previously
      # in total inches.  
      elif var_name == "height":
         session[var_name] = total_height
      
      # Creates an attribute using the name of the variable   
      else:
        session[var_name] = request.form[var_name]
        
    
    # If email is unique, create the user in the database.
    if not checkEmail(session["email"]):
        
        # Stores the new user's data.  
        createUser(session["fname"], 
                   session["lname"], 
                   session["email"],
                   session["password"], 
                   session["gender"], 
                   session["birth-day"], 
                   session["birth-month"], 
                   session["birth-year"], 
                   session["height"])
        
        return redirect(url_for('main.signup_success'))
        
    else:
        return render_template("signup.html", loginFailure=True)


# User dashboard page
@main.route("/app")
def dashboard():
  
  try:
    
    # Attempts to retrieve the first name, last name, email, and 
    # password of the user. 
    fname = session["fname"]
    lname = session["lname"]
    email = session['email']
    password = session['password']
    
    # What does this line do? -Albert
    session.clear()
    
    return render_template("app.html", 
                           email = email, 
                           password = password, 
                           fname = fname,
                           lname = lname)
  except:
      return redirect(url_for('main.login'))


app.register_blueprint(main)


#=======================================================================

if __name__ == "__main__":
    app.run(debug=True)
    app.run()


