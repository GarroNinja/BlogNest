from flask import render_template, url_for, flash, redirect, request
from blognest import app, db, bcrypt
from blognest.forms import RegistrationForm, LoginForm
from blognest.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')