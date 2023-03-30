from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from json import load
from src.common import logging_serial

auth = Blueprint('auth', __name__)


def user_agent(request):
    with open("config.json") as config:
        return request.headers.get('User-Agent') == load(config).get("configs").get("secret-agent")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not user_agent(request):
        logging_serial(f"ALERT - Unauthorized Request From IP: {request.remote_addr}", "Warning", "User-Agent")
        return render_template("apache.html")
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                logging_serial(f"User: {user.first_name} has logged in", True, "Login")
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect!, try again.', category='error')
                logging_serial(f"Failed login attempt from IP: {request.remote_addr}", "Warning", "Login")

        else:
            flash('Incorrect!, try again.', category='error')
            logging_serial(f"Failed login attempt from IP: {request.remote_addr}", "Warning", "Login")


    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    if not user_agent(request):
        return render_template("404.html")
    logout_user()
    return redirect(url_for('auth.login'))


# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if not user_agent(request):
#         return render_template("404.html")
#     if request.method == 'POST':
#         email = request.form.get('email')
#         first_name = request.form.get('firstName')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(first_name) < 2:
#             flash('First name must be greater than 1 character.', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match.', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             new_user = User(email=email, first_name=first_name, password=generate_password_hash(
#                 password1, method='sha256'))
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(new_user, remember=True)
#             flash('Account created!', category='success')
#             logging_serial(f"Created new user, name: {first_name}", "Warning", "Sign-Up")
#             return redirect(url_for('views.home'))

#     return render_template("sign_up.html", user=current_user)
