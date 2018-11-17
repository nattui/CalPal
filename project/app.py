
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 16.11.2018

This is where the python flask code occupies
TODO: Reseach G package
TODO: Finish the dashboard page

Bug: Immediately after creating an account. the app will still not let you
login. This has something to do with data retrieval not updating
immediately after data input. 
"""

from calendar import month_name
from datetime import datetime
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
    
    # Retrieves the user's data.
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


# The first user signup page.
@main.route("/signup_page_1")
def signup_page_1():
    return render_template("signup_page_1.html")


# The first user signup page redirect.
@main.route("/signup_page_1", methods=["GET", "POST"])
def signup_page_1_redirect():
  
  # Uses a for loop to access the user's inputted
  # first name, last name, email, and password. 
  for var_name in ("fname", 
                   "lname", 
                   "email", 
                   "password"):
    session[var_name] = request.form[var_name]
   
    
  # Redirects to the second signup page if the inputted email is
  # not already in the database. 
  if not checkEmail(session["email"]):
      return redirect(url_for("main.signup_page_2"))
  
  # Otherwise, reloads the page will a failure message. 
  else:
      return render_template("signup_page_1.html", loginFailure=True)
  

# The second user signup page.
@main.route("/signup_page_2")
def signup_page_2():
  return render_template("signup_page_2.html")


# The sign up button for the second user signup page. 
@main.route("/signup_page_2", methods=["GET", "POST"])
def signup_page_2_buttons():
  
  # Retrieves the name of the action. 
  # This value will either be BACK or SIGN UP. 
  action_name = request.form.get("action")
  
  # Returns to the first sign up page if the back button was pressed.
  if action_name == "BACK":
    return redirect(url_for("main.signup_page_1"))
  
  # Creates a new user if the sign up button was pressed.
  elif action_name == "SIGN UP":
  
    # Retrieves the user's height in feet and inches and converts 
    # them to integers.  
    height_feet   = int(request.form["height-feet"])
    height_inches = int(request.form["height-inches"])
    
    # Sums the total height in inches and converts it into a string. 
    total_height = str((height_feet * 12) + height_inches)

    # Uses a for loop to iterate through every piece of user information.
    for var_name in ("gender", 
                     "birth-day", 
                     "birth-month", 
                     "birth-year", 
                     "height", 
                     "weight", 
                     "calorie-goal"):
                     
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
        
    # Creates a new user based on the user's inputted data. 
    createUser(session["fname"], 
               session["lname"], 
               session["email"],
               session["password"], 
               session["gender"], 
               session["birth-day"], 
               session["birth-month"], 
               session["birth-year"], 
               session["height"], 
               session["weight"], 
               session["calorie-goal"])
      
    # Returns to the login page and displays a success message. 
    return redirect(url_for("main.signup_success"))


# User dashboard page.
@main.route("/dashboard")
def dashboard():
  
  try:
  
    # Attempts to retrieve the first name, last name, email, and 
    # password of the user. 
    fname = session["fname"]
    lname = session["lname"]
    email = session['email']
    password = session['password']
    
    # Retrieves the current date. 
    current_date = datetime.today()
    
    # Extracts the day, month, and year into strings. 
    current_day =   str(current_date.day)
    current_month = month_name[current_date.month]
    current_year =  str(current_date.year)
    
    # Formats the current date into a sentence. 
    formatted_date = " ".join(["Today is", current_month, current_day + ",", current_year + "."])

    return render_template("app.html", 
                           email = email, 
                           password = password, 
                           fname = fname,
                           lname = lname, 
                           formatted_date = formatted_date)
  except:
    
    # Redirects to the login page otherwise. 
    return redirect(url_for("main.login"))


# Controls the buttons for the dashboard page. 
@main.route("/dashboard", methods=["GET", "POST"])
def dashboard_buttons():
  
  # Retrieves the name of the action. 
  # This value will either be EXIT or UPDATE INFO. 
  action_name = request.form.get("action")
  
  # If the update info button was pressed... 
  if action_name == "UPDATE INFO":
    
    # Redirects to the update user info page. 
    return redirect(url_for("main.update_user_info"))
    
  # If the exit button was pressed...
  elif action_name == "EXIT":
    
    # Clears all the data for the session. 
    session.clear()
    
    # Redirects to the login page. 
    return redirect(url_for("main.login"))


# The update user info page. 
@main.route("/dashboard/update_user_info")
def update_user_info(updateSuccess = False):
  return render_template("update_user_info.html", updateSuccess = updateSuccess)


# Controls the buttons for the update user info page. 
@main.route("/dashboard/update_user_info", methods=["GET", "POST"])
def update_user_info_buttons():
  
  # Retrieves the name of the action. 
  # This value will either be BACK or UPDATE. 
  action_name = request.form.get("action")
  
  # Redirects to the app page if the back button was pressed. 
  if action_name == "BACK":
    return redirect(url_for("main.dashboard"))
  
  elif action_name == "UPDATE":
    return update_user_info(updateSuccess = True)


app.register_blueprint(main)


#=======================================================================

if __name__ == "__main__":
    app.run(debug=True)
    app.run()


