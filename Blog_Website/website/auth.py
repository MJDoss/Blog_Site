from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re




auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Username not in use.', category='error')   

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()
        if(user_email):
            flash('Email already exists.', category='error')
        elif(user_username):
            flash('Username already exists.', category='error')
        elif(email == ''):
            flash('Please enter an Email.', category='error')
        elif(username == ''):
            flash('Please enter an Username.', category='error')
        elif(password == ''):
            flash('Please enter a Password.', category='error')
        elif(repassword == ''):
            flash('Please enter a confirmation Password.', category='error')
        elif (len(username) < 3):
            flash('Username is too short.', category='error')
        elif len(password) < 10:
            flash('Password must be at least 10 characters in length', category='error')
        elif password != repassword:
            flash('Password and confirmation password do not match', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account successfully made!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html")

