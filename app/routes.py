from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post

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
    form = RegistrationForm()
    # Validate form
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# Login Form
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()    
    # Validate form
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'Welcome back {form.email.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccesful. Please check username and password', 'danger')
    return render_template('login.html', title='Welcome Back!', form=form)