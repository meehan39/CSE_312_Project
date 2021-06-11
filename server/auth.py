from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Posts
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html', title="Log In")

# Login method
@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Invalid username or password. Please try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html', title="Sign Up")

# Signup method
@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')
    email_check = User.query.filter_by(email=email).first()
    username_check = User.query.filter_by(username=username).first()

    if email_check:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    elif username_check:
        flash('This username is already taken')
        return redirect(url_for('auth.signup'))
    elif password != repeat_password:
        flash('Passwords do not match')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'), avatar = 'default.png')
    db.session.add(new_user)
    db.session.commit()
    user_list=User.query.all()
    print(user_list)
    return redirect(url_for('auth.login'),)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
