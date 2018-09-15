# TODO: Reseach G package

# This is where the python flask code occupies

from flask import Flask, render_template, redirect, url_for, request, Blueprint, session
from modules.reader import checkLogin, checkEmail, getDatabase, userCreation

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

    # If user information matches the information in the database, continue to application
    if checkLogin(session['email'], session['password']):
        return redirect(url_for('main.dashboard'))
    else:
        return render_template("login.html", loginFailure=True)

# User signin page
@main.route("/signup")
def signup():
    return render_template("signup.html")

# BUG Keeps name of previous user who signed up
# If the user is sucessfully created
@main.route("/success")
def signup_success():
    return render_template("login.html", userCreation=True)

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


# TODO: Finish the dashboard page
# User dashboard page
@main.route("/app")
def dashboard():
    try:
        email = session['email']
        password = session['password']
        session.clear()
        return render_template("app.html", email=email, password=password)
    except:
        return redirect(url_for('main.login'))



app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
    app.run()
