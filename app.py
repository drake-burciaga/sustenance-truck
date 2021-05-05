from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY']= '27795525de510704b1bdd2f0349a5e02'

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
@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

# Login Form
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Welcome Back!', form=form)

if __name__ == '__main__':
    app.run(debug=True)