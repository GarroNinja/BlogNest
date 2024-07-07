from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '1e772b7b84f34b27b83f916e2d46a641'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

posts = [
    {
        "author": "Rithvik A",
        "title": "Rediscovering Nature: A Weekend Getaway in the Digital Age",
        "content": "In our fast-paced, technology-driven lives, finding time to reconnect with nature can seem like a distant dream. Yet, spending a weekend immersed in the great outdoors can work wonders for our mental and physical well-being. Whether it’s a hike through a serene forest, a camping trip under the stars, or simply a day at a local park, nature offers a perfect escape from the digital grind. This past weekend, I traded my screen for scenic trails and found a refreshing sense of peace and clarity that only nature can provide. Disconnecting from devices to reconnect with the world around us isn’t just a break; it’s a vital reset for the soul.",
        "date_posted": "July 1, 2024"
    },
    {
        "author": "Garro",
        "title": "Culinary Adventures: Exploring the World Through Food",
        "content": "In our fast-paced, technology-driven lives, finding time to reconnect with nature can seem like a distant dream. Yet, spending a weekend immersed in the great outdoors can work wonders for our mental and physical well-being. Whether it’s a hike through a serene forest, a camping trip under the stars, or simply a day at a local park, nature offers a perfect escape from the digital grind. This past weekend, I traded my screen for scenic trails and found a refreshing sense of peace and clarity that only nature can provide. Disconnecting from devices to reconnect with the world around us isn’t just a break; it’s a vital reset for the soul.",
        "date_posted": "July 2, 2024"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash("You have been logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful, Please check email and password", 'danger')
    return render_template('login.html', title="Login", form=form)

if __name__ == '__main__':
    app.run(debug=True)
