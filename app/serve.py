# Spin The Wheel -- Matthew Chen, Sakina Raza, Caroline Tham, Efaz Khan
# SoftDev  P00 -- Scenario Sigma
# Target ship date: 2026-11-18

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
import db

app = Flask(__name__)
# Set a secret key so Flask can safely sign session cookies
app.secret_key = "secret_key"

db.init_db()

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
    if db.check_login(username, password):
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
    if not db.add_user(username, password):
        return render_template('response.html', message="Username already exists! Try logging in.")
    return render_template('response.html', message="Account successfully created! Please return home to log in.")

@app.route("/profile")
def profile():
    # Check if logged in AND if the user actually exists in the fresh database
    if "username" not in session or db.get_user_id(session["username"]) is None:
        session.pop("username", None)  # Clear ghost session
        return redirect(url_for('login'))
    return render_template('profile.html', username=session["username"])

@app.route("/new", methods=["GET", "POST"])
def new():
    if "username" not in session or db.get_user_id(session["username"]) is None:
        session.pop("username", None)
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
    if "username" not in session or db.get_user_id(session["username"]) is None:
        session.pop("username", None)
        return redirect(url_for('login'))
    browseable_stories = db.get_browsable_stories(session["username"])
    return render_template('browse.html', stories=browseable_stories)

@app.route("/add/<int:story_id>", methods=["GET", "POST"])
def add(story_id):
    if "username" not in session or db.get_user_id(session["username"]) is None:
        session.pop("username", None)
        return redirect(url_for('login'))

    story = db.get_story(story_id)
    if not story:
        return render_template('response.html', message="Story does not exist.")

    if request.method == "GET":
        latest_text = db.get_latest_contribution(story_id)
        return render_template('add.html', story_id=story_id, story_title=story["title"], latest_text=latest_text)

    body = request.form.get('body')
    if not body:
        return render_template('response.html', message="Contribution cannot be empty.")

    success = db.add_contribution(session["username"], story_id, body)
    if not success:
        return render_template('response.html', message="You have already contributed to this story!")

    return redirect(url_for('profile'))

# logout is POST because the logout button is a form with method="POST"
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.init_db()
    app.debug = True
    app.run()