from collections import UserString
from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired, Regexp, ValidationError
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_pymongo import PyMongo
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
import uuid
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = "my super secret key"

app.config['MONGO_URI'] = 'mongodb+srv://rowdyrover:5LoCaB1aMpVCxsso@cluster0.nppjde0.mongodb.net/flaskDatabase?retryWrites=true&w=majority'

app.config['UPLOAD_FOLDER'] = 'uploads'


#setup mongodb
mongodb_client = PyMongo(app)

db = mongodb_client.db

#Forms
class UserForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired()])
  submit = SubmitField("Submit")

class SignUpForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired(), Regexp('^[a-zA-Z0-9]+$', message="Name can only contain letters and numbers")])
  password = StringField("Password", validators=[DataRequired()])
  submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  password = StringField("Password", validators=[DataRequired()])
  submit = SubmitField("Login")

class NameForm(FlaskForm):
	name = StringField("What's Your Name", validators=[DataRequired()])
	submit = SubmitField("Submit")

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
  if request.method == 'POST':
    form = UserForm()
    name = form.name.data
    email = form.email.data

    db.users.insert_one({
       "name": name,
       "email": email,
       "date_created": datetime.utcnow()
    })
    flash("User Addded Successfully!")
    return redirect("/")
  else:
    form = UserForm()
  return render_template("add_user.html", form=form)

@app.route('/user/signup', methods=['GET', 'POST'])
def sign_up():
  form = SignUpForm()

  # Validate form data
  if form.validate_on_submit():
    name = form.name.data
    password = form.password.data

    # Create the user object
    user = {
        "_id": uuid.uuid4().hex,
        "name": name,
        "password": password
    }

    #Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing user with the same name
    existing_user = db.users.find_one({ "name": user['name'] })
    if existing_user:
      flash("User with this name already exists")
      return redirect(url_for('sign_up'))

    # Insert the user into the database
    db.users.insert_one(user)

    # Start the session
    session['logged_in'] = True
    session['user'] = {
        "_id": user["_id"],
        "name": user["name"]
    }

    return redirect(url_for('user', name=name))

  return render_template("sign_up.html", form=form)

@app.route('/user/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    name = form.name.data
    password = form.password.data
    
    # Retrieve user from the database based on the provided name
    user = db.users.find_one({ "name": name })

    # Verify if the user exists and the password is correct
    if user and pbkdf2_sha256.verify(password, user['password']):
      # Start session and redirect to user page
      session['logged_in'] = True
      session['user'] = {
        "_id": user["_id"],
        "name": user["name"]
      }
      return redirect(url_for('user', name=name))
    else:
      flash("Invalid username or password. Please try again.")

  return render_template("login.html", form=form)

@app.route('/user/logout')
def logout():
  session.clear()
  return redirect(url_for('login'))

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/user/<name>')
def user(name):
  if 'logged_in' in session:
    return render_template("user.html", name=name)
  else:
    flash("You need to log in first.")
    return redirect(url_for('login'))

#@app.route('/user/<name>/data', methods=['POST', 'GET'])


@app.route('/upload', methods=['POST', 'GET'])
def handle_data():
    if request.method == 'POST':
        if 'file' in request.files:
          file = request.files['file']
          # Do something with the file, such as saving it to disk or processing it
          db.uploads.insert_one({
              "file" : file,
             "date_created" : datetime.utcnow()
            })
          return 'File uploaded successfully', 200

    # Handle other HTTP methods (GET, POST) as needed
    if request.method == 'PUT':
      if 'file' in request.files:
          file = request.files['file']
          # Do something with the file, such as saving it to disk or processing it
          db.uploads.insert_one({
              "file" : file,
             "date_created" : datetime.utcnow()
            })
          return 'File uploaded successfully', 200
    # For demonstration purposes, we'll return a message for other methods
    return request.method, 600

#Error Pages
@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template("500.html"), 500

@app.route('/name', methods=['GET', 'POST'])
def name():
  name = None
  form = NameForm()
  if form.validate_on_submit():
    name = form.name.data
    form.name.data = ''
    flash("Form Submitted Successfully!")

  return render_template("name.html", name=name, form=form)

@app.route('/potree')
def potree_viewer():
  return render_template('potree_viewer.html')

