from collections import UserString
from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_pymongo import PyMongo
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
import uuid
import os

app = Flask(__name__)

#db = client.users_db
#todos = db.todos

#database_path = os.path.join(app.root_path, 'instance', 'users.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://default:ZFu7KC3xYhUg@ep-red-sun-42046104.us-east-1.postgres.vercel-storage.com:5432/verceldb'
#"postgres://default:ZFu7KC3xYhUg@ep-red-sun-42046104.us-east-1.postgres.vercel-storage.com:5432/verceldb"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:iCYTEGcgJBNSqJP0ZumXxkT@localhost/our_users'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = "my super secret key"
app.config['MONGO_URI'] = 'mongodb+srv://rowdyrover:5LoCaB1aMpVCxsso@cluster0.nppjde0.mongodb.net/flaskDatabase?retryWrites=true&w=majority'

#setup mongodb
mongodb_client = PyMongo(app)

db = mongodb_client.db


#db.init_app(app)
#db = SQLAlchemy(app)
#app.app_context().push()
#with app.app_context():
#  db.create_all()

#class Users(db.Model):
  #id = db.Column(db.Integer, primary_key=True)
  #name = db.Column(db.String(50), nullable=False) #cant be blank
  #email = db.Column(db.String(100), nullable=False, unique=True)
  #date_added = db.Column(db.DateTime, default=datetime.utcnow)

  #def __repr__(self):
    #return '<Name %r>' % self.name


#Forms
class UserForm(FlaskForm):
  name = StringField("Name", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired()])
  submit = SubmitField("Submit")

def no_spaces(form, field):
  if ' ' in field.data:
    raise ValidationError('Name cannot contain spaces')

class SignUpForm(FlaskForm):
  name = StringField("Name", [DataRequired(), no_spaces])
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
    #session['logged_in'] = True
    #session['user'] = {
        #"_id": user["_id"],
        #"name": user["name"]
    #}

    return redirect(url_for('user', name=name))

  # If form validation fails, redirect back to sign-up page
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
  return redirect(url_for('sign_up'))

#@app.route('/user/add', methods=['GET', 'POST'])
#def add_user():
  #if request.method == 'POST':
    #form = UserForm()
    #name = form.name.data
    #email = form.email.data

    #db.user.insert_one({
      #"name": name,
      #"email": email,
      #"date_completed": datetime.utcnow()
    #})
    #flash("User Added Successfully!")
  #else:
    #form = UserForm()
  #return render_template("add_user.html", form=form)
     
#@app.route('/user/add', methods=['GET', 'POST'])
#def add_user():
  #name = None
  #form = UserForm()
  #if form.validate_on_submit():
    #user = Users.query.filter_by(email=form.email.data).first()
    #if user is None:
      #user = Users(name=form.name.data, email=form.email.data)
      #db.session.add(user)
      #db.session.commit()
    #name = form.name.data
    #form.name.data = ''
    #form.email.data = ''
    #flash("User Added Successfully!")
  #our_users = Users.query.order_by(Users.date_added)
  #return render_template("add_user.html", form=form, name=name, our_users=our_users)

@app.route('/')
def index():
  first_name = "Rowdy"
  return render_template("index.html", first_name=first_name)

@app.route('/user/<name>')

def user(name):
  return render_template("user.html", name=name)

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

