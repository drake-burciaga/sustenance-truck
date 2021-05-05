from flask import Flask, render_template
app = Flask(__name__)

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
    return render_template('about.html', title='fucking tets')

if __name__ == '__main__':
    app.run(debug=True)