#!/usr/bin/python3
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Last Revised by Nhat Nguyen: 24.27.2018 

This is where the python flask code occupies
TODO: Finish the dashboard page
"""

from calendar import month_name
from datetime import datetime

from flask import (Flask, 
                   render_template, 
                   redirect, 
                   url_for, 
                   request, 
                   Blueprint, 
                   session)
                   
from modules.conversion import (monthNameToNumber,
                            monthNumberToName,
                            mergeHeight, 
                            splitHeight)
                            
from modules.reader import (checkLogin, 
                            checkEmail, 
                            getUserDatabase, 
                            getUserData,
                            createUser, 
                            writeNewUserData)

from modules.FoodReader import FoodReader
from modules.ExerciseReader import ExerciseReader

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
    
    # Attempts to retrieve the user's data.
    try: 
      user_data = getUserData(session["email"])
    
    # Returns displays an error message is the email is not currently registered.
    except IndexError:
      return render_template("login.html", unusedEmail = True)
    
    # Assigns the remaining as attributes to session. 
    for var_index, var_name in enumerate(("fname", 
                                          "lname", 
                                          "email",
                                          "password",
                                          "gender", 
                                          "birth-day", 
                                          "birth-month", 
                                          "birth-year", 
                                          "height", 
                                          "weight", 
                                          "calorie-goal")):
      session[var_name] = user_data[var_index]
      
    # Assigns the number for rows for exercise and food inputs.
    # The default number is 3. 
    session["exercise_rows"] = 3
    session["food_rows"] = 3
    
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
  for var_name in ("fname", "lname", "email", "password"):
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
    total_height = str(mergeHeight(height_feet, height_inches))

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
          
        # Converts the the user's birth month to its
        # corresponing number. 
        month_num = monthNameToNumber(month_name)
        
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
    createUser([session["fname"], 
                session["lname"], 
                session["email"],
                session["password"], 
                session["gender"], 
                session["birth-day"], 
                session["birth-month"], 
                session["birth-year"], 
                session["height"], 
                session["weight"], 
                session["calorie-goal"]])
      
    # Returns to the login page and displays a success message. 
    return redirect(url_for("main.signup_success"))


# User dashboard page.
@main.route("/dashboard")
def dashboard():
  
  # Attempts to retrieve the first name, last name, email, and 
  # password of the user. 
  try:
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
    
    # Retrieves the list of exercises and foods.
    food_obj = FoodReader()
    exercise_obj = ExerciseReader()

    food_list = food_obj.food_column
    exercise_list = exercise_obj.exercise_column
    
    return render_template("dashboard.html", 
                           email          = email, 
                           password       = password, 
                           fname          = fname,
                           lname          = lname, 
                           formatted_date = formatted_date, 
                           exercise_list  = exercise_list,
                           food_list      = food_list, 
                           exercise_rows  = session["exercise_rows"], 
                           food_rows      = session["food_rows"])
  except:
    
    # Redirects to the login page otherwise. 
    return redirect(url_for("main.login"))


# Controls the buttons for the dashboard page. 
@main.route("/dashboard", methods=["GET", "POST"])
def dashboard_buttons():
  
  # Retrieves the name of the action. 
  # This value will either be ADD_FOOD_ROW, SUB_FOOD_ROW, 
  # EXIT, or UPDATE INFO. 
  action_name = request.form.get("action")
  
  # If the add food row button was pressed... 
  if action_name == "ADD_FOOD_ROW":
    
    # Increments the number of food rows.
    session["food_rows"] += 1
    
    # Reloads the dashboard page.
    return dashboard()
  
  # If the subtract food row button was pressed... 
  elif action_name == "SUB_FOOD_ROW":
    
    # Decrements the number of food rows if there are more than 3 rows.
    if session["food_rows"] > 3:
      session["food_rows"] -= 1
    
    # Reloads the dashboard page.
    return dashboard()
  
  # If the update info button was pressed... 
  elif action_name == "UPDATE INFO":
    
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
def update_user_info(updateSuccess = False, usedEmail = False):
  
  # Calculates the user's height in both feet and inches.
  split_height  = splitHeight(int(session["height"]))
  height_feet   = split_height[0]
  height_inches = split_height[1]

  return render_template("update_user_info.html", 
                         fname         = session["fname"],
                         lname         = session["lname"],
                         email         = session["email"], 
                         password      = session["password"],
                         gender        = session["gender"],
                         birth_day     = session["birth-day"],
                         birth_month   = session["birth-month"],
                         birth_year    = session["birth-year"],
                         height_feet   = height_feet,
                         height_inches = height_inches,
                         weight        = session["weight"],
                         calorie_goal  = session["calorie-goal"],
                         updateSuccess = updateSuccess, 
                         usedEmail     = usedEmail)


# Controls the buttons for the update user info page. 
@main.route("/dashboard/update_user_info", methods=["GET", "POST"])
def update_user_info_buttons():
  
  # Retrieves the name of the action. 
  # This value will either be BACK or UPDATE. 
  action_name = request.form.get("action")
  
  # Redirects to the app page if the back button was pressed. 
  if action_name == "BACK":
    return redirect(url_for("main.dashboard"))
  
  # If the update info button was pressed...
  elif action_name == "UPDATE":
    
    # Retrieves the inputted email. 
    new_email = request.form["email"]
    
    # Checks if the inputted email is either unused in the current database
    # or is the user's current email.
    viable_email = (not checkEmail(new_email)) or \
                   (new_email == session["email"])
    
    # If the inputted email was viable...
    if viable_email:
    
      # Retrieves all the new inputted values. 
      new_fname         = request.form["fname"]
      new_lname         = request.form["lname"]
      new_password      = request.form["password"]
      new_gender        = request.form["gender"]
      new_birth_day     = request.form["birth-day"]
      new_birth_month   = monthNameToNumber(request.form["birth-month"]) # Converts month name to number. 
      new_birth_year    = request.form["birth-year"]
      new_height_feet   = int(request.form["height-feet"])
      new_height_inches = int(request.form["height-inches"])
      new_weight        = request.form["weight"]
      new_calorie_goal  = request.form["calorie-goal"]
      
      # Calculates the new, total height. 
      new_total_height = mergeHeight(new_height_feet, new_height_inches)
      
      # A list of the new user data. 
      new_user_data = [new_fname, 
                       new_lname, 
                       new_email, 
                       new_password, 
                       new_gender, 
                       new_birth_day, 
                       new_birth_month, 
                       new_birth_year, 
                       new_total_height, 
                       new_weight, 
                       new_calorie_goal]
      
      # Writes the new data to database.xlsx. 
      writeNewUserData(session["email"], new_user_data)
      
      # Assigns the new data as attributes to session. 
      for var_index, var_name in enumerate(("fname", 
                                            "lname", 
                                            "email",
                                            "password",
                                            "gender", 
                                            "birth-day", 
                                            "birth-month", 
                                            "birth-year", 
                                            "height", 
                                            "weight", 
                                            "calorie-goal")):
        session[var_name] = new_user_data[var_index]
      
      # Reloads the same page except with an update successful message. 
      return update_user_info(updateSuccess = True)
  
    # Displays an error message is the email is already used. 
    else:
      return update_user_info(usedEmail = True)

app.register_blueprint(main)


#=======================================================================

if __name__ == "__main__":
    app.run(debug=True)
    app.run()


