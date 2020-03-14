import os

from flask import Flask, session, render_template, url_for, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__, static_url_path='/static')

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template ("index.html")

@app.route("/signup")
def signup():
    return render_template ("signup.html")

@app.route("/signup-success", methods=["POST"])
def signup_success():
    #Get information from the signup page
    firstName = request.form.get("first-name")
    lastName = request.form.get("last-name")
    email = request.form.get("email")
    password = request.form.get("password")

    #add form information to database
    db.execute("INSERT INTO users (firstname, lastname, email, password) VALUES (:firstname, :lastname, :email, :password)",
    {"firstname": firstName, "lastname": lastName, "email": email, "password": password})
    db.commit()


    return render_template ("signup-success.html", firstname=firstName)

@app.route("/login")
def login():
    return render_template ("login.html")

@app.route("/home", methods=["POST"])
def home():
    #Get information from the signup page
    email = request.form.get("email")
    password = request.form.get("password")

    #check if username and password are correct
    if db.execute("SELECT * FROM users WHERE email = :email AND password = :password", {"email": email, "password": password}).rowcount == 0:
        return render_template("error.html", message="Incorrect username and/or password. Please try again")
        db.commit()
    else:
        return render_template ("home.html")

@app.route("/search", methods=["POST"])
def search():
    return render_template ("search-result.html")

@app.route("/book")
def book():
    return render_template ("book.html")

@app.route("/error")
def error():
    return render_template ("error.html")