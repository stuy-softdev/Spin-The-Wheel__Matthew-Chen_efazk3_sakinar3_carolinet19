# Spin The Wheel -- Matthew Chen, Sakina Raza, Caroline Tham, Efaz Khan
# SoftDev  P00 -- Scenario Sigma
# Target ship date: 2026-11-18

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
import csv
import os
import db

csvfile = "users.csv"

app = Flask(__name__)
# Set a secret key so Flask can safely sign session cookies
app.secret_key = "secret_key"

# Creates the CSV file with headers ONLY if it doesn't exist yet
# ****change this later to use SQL
def init_csv():
    if not os.path.exists(csvfile):
        with open(csvfile, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=['USERNAMES', 'PASSWORDS'])
            writer.writeheader()


# Checks the CSV to see if a username and password combo is on it
# ****change this later to use SQL
def checkPassword(username, password):
    with open(csvfile, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if username == row.get("USERNAMES") and password == row.get("PASSWORDS"):
                return True
    return False

@app.route("/")
def index():
    # If user is logged in, show the welcome/logout page
    if "username" in session:
        return redirect(url_for('profile'))
    else:
        # Otherwise, show the landing page with the Login / Create account buttons
        return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    # GET = they just want to see the page
    if request.method == "GET":
        return render_template('login.html')

    # Otherwise it's a POST: they submitted the form
    username = request.form.get('username')
    password = request.form.get('password')

    if checkPassword(username, password):
        session["username"] = username  # Establish session state
        return redirect(url_for('profile'))
    else:
        return render_template('response.html', message="Invalid username or password. Please try again.")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')

    username = request.form.get('username')
    password = request.form.get('password')

    # Checks if either field is empty
    if not username or not password:
        return render_template('response.html', message="Username and password cannot be empty.")

    # Check if username already exists
    with open(csvfile, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if username == row.get("USERNAMES"):
                return render_template('response.html', message="Username already exists! Try logging in.")

    # Append the new user to the CSV file (mode 'a' = append)
    with open(csvfile, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=['USERNAMES', 'PASSWORDS'])
        writer.writerow({'USERNAMES': username, 'PASSWORDS': password})

    return render_template('response.html', message="Account successfully created! Please return home to log in.")

@app.route("/profile")
def profile():
    if "username" not in session:
        # redirect to login page if not logged in
        return redirect(url_for('login'))
    else:
        return render_template('profile.html', username=session["username"])

@app.route("/new", methods=["GET", "POST"])
def new():
    if "username" not in session:
        # redirect to login page if not logged in
        return redirect(url_for('login'))

    if request.method == "GET":
        return render_template('new.html')

    title = request.form.get('title')
    body = request.form.get('body')
    if not title or not body:
        return render_template('response.html', message="Title and text cannot be empty.")

    db.create_story(session["username"], title, body)
    return redirect(url_for('profile'))

@app.route("/browse")
def browse():
    if "username" not in session:
        # redirect to login page if not logged in
        return redirect(url_for('login'))

    browseable_stories = db.get_browsable_stories(session["username"])
    browseable_stories = [(1, "Story 1"), (2, "Story 2")] # just for testing purposes
    return render_template('browse.html', stories=browseable_stories)

@app.route(f"/add/1")
def add():
    if "username" not in session:
        # redirect to login page if not logged in
        return redirect(url_for('login'))
    db.get_latest_contribution(1)
    return render_template('profile.html')

# logout is POST because the logout button is a form with method="POST"
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_csv()   # safe now: only creates the file if it's missing
    app.debug = True
    app.run()
