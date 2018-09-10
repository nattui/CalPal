# This is where the python flask code occupies

from flask import Flask, render_template, redirect, url_for, request, Blueprint, session
from modules.reader import checkLogin

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

main = Blueprint("main", __name__)


# Main page for login
@main.route("/")
def home():
  return render_template("login.html")

# User login logic
@main.route("/", methods=["GET", "POST"])
def login():
  # Stores user information 
  session["email"] = request.form["email"]
  session["password"] = request.form["password"]

  # If user information matches the information in the database, continue to application
  if checkLogin(session['email'], session['password']):
    return redirect(url_for('main.dashboard'))
  else:
    return render_template("login.html", loginFailure=True)

# TODO: Finish the dashboard page
# Dashboard page
@main.route("/app")
def dashboard():
  return render_template("app.html", email=session["email"], password=session["password"])


app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
