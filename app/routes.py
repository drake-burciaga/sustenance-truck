import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


# Home Page
@app.route('/')
@app.route('/home')
def home():
    # show all posts from database
    posts = Post.query.all()
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
            next_page = request.args.get('next')
            # redirect to next page if it exists
            # or if it is none or false, redirect to home page
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccesful. Please check email and password', 'danger')
    return render_template('login.html', title='Welcome Back!', form=form)

# Log out
@app.route('/logout')
def logout():
    "if user is logged in, they will have option to log out"
    logout_user()
    return redirect (url_for('home'))

def save_picture(form_picture):
    "save user's profile picture"
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resize picture
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # save resized image
    i.save(picture_path)

    return picture_fn


# Account
@app.route('/account', methods=['GET', 'POST'])
@login_required
# need to login to access this page
def account():
    form = UpdateAccountForm()
    # if form is validated
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        # enter user's username or email change
        current_user.username = form.username.data
        current_user.email = form.email.data
        # commit to the database
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
          
    # if GET request, populate current username/email into form
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

# New User Post
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    # if form is validated
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        # save post to database
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

# Route to each unique post
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# Route to update post
@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        # populate existing data
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

# Delete Post
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    # delete post
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect (url_for('home'))