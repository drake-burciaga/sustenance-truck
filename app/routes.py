from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
    'author': 'Drake B',
    'title': 'Post 1',
    'content': 'First Post',
    'date_posted': "today"
    },
    {
    'author': 'Chase B',
    'title': 'Post 2',
    'content': 'Second Post',
    'date_posted': "today"
    }
]

# Home Page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

# About Us 
@app.route('/about')
def about():
    return render_template('about.html', title='About')

# Register User Form
@app.route('/register', methods=['GET', 'POST'])
def register():

    # if user is logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    # Validate form
    if form.validate_on_submit():
        # password hash with bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # assign hashed password to user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Login Form
@app.route('/login', methods=['GET', 'POST'])
def login():

    # if user is logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()    
    # Validate form | Login with email
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if the user exists in the db and the password is correct - login
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccesful. Please check email and password', 'danger')
    return render_template('login.html', title='Welcome Back!', form=form)

# Log out
@app.route('/logout')
def logout():
    "if user is logged in, they will have option to log out"
    logout_user()
    return redirect (url_for('home'))

# Account
@app.route('/account')
@login_required
# need to login to access this page
def account():
    return render_template('account.html')