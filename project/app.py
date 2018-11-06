
"""
CalPal: A calorie tracking app.
Written by Nhat Nguyen and Albert Ong.
CMPE 131
Revision: 05.11.2018

This is where the python flask code occupies
TODO: Reseach G package
TODO: Finish the dashboard page
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
                            returnFirstLastName,
                            userCreation)

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
    names = returnFirstLastName(session["email"])
    
    # Assigns the first and last names as attributes to session. 
    session["fname"] = names[0]
    session["lname"] = names[1]
    
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

    # Stores signup user information
    session["fname"] = request.form["fname"]
    session["lname"] = request.form["lname"]
    session["email"] = request.form["email"]
    session["password"] = request.form["password"]
    
    # If email is unique, create the user in the database
    if not checkEmail(session["email"]):
        userCreation(session["fname"], session["lname"], session["email"], session["password"])
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


