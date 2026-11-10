from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
import csv
import os

csvfile = "users.csv"

app = Flask(__name__)
# Set a secret key so Flask can safely sign session cookies
app.secret_key = "super_secret_key_amc"

# Helper function to ensure the CSV file exists with headers
def init_csv():
    if os.path.exists(csvfile): # Edit: removed the "not" keyword from not os.path.exists(csvfile)
        with open(csvfile, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=['USERNAMES', 'PASSWORDS'])
            writer.writeheader()

@app.route("/")
def disp_loginpage():
    # If user is logged in, show the welcome/logout page
    if "username" in session:
        return render_template('logout.html', username=session["username"])
    # Otherwise, show the login/create account page
    return render_template('login.html')

@app.route("/auth")
def authenticate():
    username = request.args.get('username')
    password = request.args.get('password')

    # Check if user exists and password matches
    if checkPassword(username, password):
        session["username"] = username  # Establish session state, yay!
        return redirect(url_for('disp_loginpage'))

    # If info is wrong, use response.html to display the error
    return render_template('response.html', message="Invalid username or password. Please try again.")

def checkPassword(username, password):
    #init_csv()
    with open(csvfile, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if username == row.get("USERNAMES") and password == row.get("PASSWORDS"):
                return True
    return False

@app.route("/acc")
def createAccount():
    #init_csv()
    username = request.args.get('username')
    password = request.args.get('password')

    # Checks if either parameter is empty
    if not username or not password:
        return render_template('response.html', message="Username and password cannot be empty.")

    # Check if username already exists
    with open(csvfile, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if username == row.get("USERNAMES"):
                return render_template('response.html', message="Username already exists! Try logging in.")

    # Append the new user to the CSV file (using mode 'a') so cool ...
    with open(csvfile, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=['USERNAMES', 'PASSWORDS'])
        writer.writerow({'USERNAMES': username, 'PASSWORDS': password})

    return render_template('response.html', message="Account successfully created! Please return home to log in.")

# logout uses the POST method, so it raises an error if Flask is restricted to only GET (default setting)
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # Clear the session username cookie so cool . ..
    session.pop("username", None)
    return redirect(url_for('disp_loginpage'))

if __name__ == "__main__":
    # commented out init_csv() because it deletes data from previous session. For example, if i create an account when I open the flask app and then shut down the app, the account would be deleted from users.csv
    #init_csv()
    app.debug = True
    app.run()
