#!/usr/bin/python3
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 01.12.2018 

app.py
This is where the python flask code occupies
"""

from calendar import month_name
from datetime import datetime

from flask import *
from modules.module import *
from modules.reader import *
from modules.FoodReader import (getFoodDatabase,
                                getFoodCalories)
from modules.ExerciseReader import (getExerciseDatabase,
                                    getExerciseCalories)

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

main = Blueprint("main", __name__)

# Redirects to the login page
@main.route("/")
def index():
    session["calorie_food_list"] = []
    session["calorie_exercise_list"] = []
    session["count_exercise_calorie"] = 0
    return redirect(url_for('main.login'))


# User login page
@main.route("/login")
def login():
    session["calorie_food_list"] = []
    session["calorie_exercise_list"] = []
    session["count_exercise_calorie"] = 0
    return render_template("login.html")


# Handles the login page logic
@main.route("/login", methods=["GET", "POST"])
def login_redirect():

    # Stores login user information 
    email_input = request.form["email"]
    password_input = request.form["password"]
    
    # Attempts to retrieve the user's data.
    try: 
      user_data = getUserData(email_input)
    
    # Returns displays an error message is the email is not currently registered.
    except IndexError:
      return render_template("login.html", unusedEmail = True)
    
    # If user information matches the information in the database, continue to application
    if checkLogin(email_input, password_input):
    
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
        
      # Loads the dashboard page.
      return redirect(url_for('main.dashboard'))
    
    # Otherwise loads the login page with a login failure message. 
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
  
  # Retrieves the current date. 
  current_date = datetime.today()
  
  # Extracts the day, month, and year into strings. 
  current_day =   str(current_date.day)
  current_month = month_name[current_date.month]
  current_year =  str(current_date.year)
  
  # Formats the current date into a sentence. 
  formatted_date = " ".join(["Today is", current_month, current_day + ",", current_year + "."])

  session["foratted_date"] = formatted_date
  
  # Retrieves the list of exercises and foods.
  food_list = getFoodDatabase()[1]
  exercise_list = getExerciseDatabase()[0]
  
  return render_template("dashboard.html", 
                         fname          = session["fname"],
                         lname          = session["lname"], 
                         formatted_date = formatted_date, 
                         exercise_list  = exercise_list,
                         food_list      = food_list)


# Controls the buttons for the dashboard page. 
@main.route("/dashboard", methods=["GET", "POST"])
def dashboard_buttons():
  
  # Retrieves the name of the action. 
  # This value will either be SUBMIT, EXIT, or UPDATE INFO. 
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
  
  # If the sumbit button was pressed...
  elif action_name == "SUBMIT_FOODS":
    
    # Retrieves the name of the food and the number of ounces consumed. 
    food = request.form["food"]
    ounce = request.form["ounce"]
    
    
    calorie_food_list = session["calorie_food_list"]
    count_food_calorie = 0
    
    # Calculated the number of calories gained. 
    calories = getFoodCalories(food, float(ounce))
    
    if (calories >= 0):
      calorie_food_list.append([food, calories])
      session["calorie_food_list"] = calorie_food_list
        
    for calories in calorie_food_list:
      count_food_calorie = count_food_calorie + int(calories[1])
      session["count_food_calorie"] = count_food_calorie

    total_calories = session["count_food_calorie"] - session["count_exercise_calorie"]


    # Retrieves the list of exercises and foods.
    session["food_list"] = getFoodDatabase()[1]
    session["exercise_list"] = getExerciseDatabase()[0]

    return render_template("dashboard.html", 
                          fname          = session["fname"],
                          lname          = session["lname"], 
                          formatted_date = session["foratted_date"],
                          food_list      = session["food_list"], 
                          exercise_list  = session["exercise_list"],
                          calorie_food_list   = session["calorie_food_list"],
                          calorie_exercise_list = session["calorie_exercise_list"],
                          total_calories = int(total_calories))


  # EXERCISE
  elif action_name == "SUBMIT_EXERCISE":
    exercise = request.form["exercise"]
    minute = request.form["minute"]

    calorie_exercise_list = session["calorie_exercise_list"]
    count_exercise_calorie = 0

    calories = getExerciseCalories(exercise, float(minute), session["weight"])
    if (calories >= 0):
      calorie_exercise_list.append([exercise, calories])
      session["calorie_exercise_list"] = calorie_exercise_list

    for calories in calorie_exercise_list:
      count_exercise_calorie = count_exercise_calorie + int(calories[1])
      session["count_exercise_calorie"] = count_exercise_calorie

    total_calories = session["count_food_calorie"] - session["count_exercise_calorie"]

    return render_template("dashboard.html", 
                        fname          = session["fname"],
                        lname          = session["lname"], 
                        formatted_date = session["foratted_date"],
                        food_list      = session["food_list"], 
                        exercise_list  = session["exercise_list"],
                        calorie_food_list = session["calorie_food_list"],
                        calorie_exercise_list = session["calorie_exercise_list"],
                        total_calories = int(total_calories))


# The update user info page. 
@main.route("/dashboard/update_user_info")
def update_user_info(updateSuccess = False, usedEmail = False):
  
  # Calculates the user's height in both feet and inches.
  split_height  = splitHeight(int(session["height"]))
  height_feet   = split_height[0]
  height_inches = split_height[1]
  
  # ~ print(session["birth-day"])
  # ~ print(session["birth-month"])
  # ~ print(session["birth-year"])
  # ~ print(height_feet)
  # ~ print(height_inches)
  
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


