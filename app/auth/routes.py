from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import LoginForm, UserCreationForm

#import login funcitonality
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

# import models
from app.models import User

auth = Blueprint('auth', __name__, template_folder='authtemplates')

from app.models import db

@auth.route('/login', methods = ["GET","POST"])
def logMeIn():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            # Query user based off of username
            user = User.query.filter_by(username=username).first()
            print(user.username, user.password, user.id)
            if user:
                # compare passwords
                if check_password_hash(user.password, password):
                    flash('You have successfully logged in!', 'success')
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    flash('Incorrect username/password combination.', 'danger')
            else:
                flash('User with that username does not exist.', 'danger')

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logMeOut():
    flash("Successfully logged out.", 'success')
    logout_user()
    return redirect(url_for('auth.logMeIn'))

@auth.route('/signup', methods=["GET", "POST"])
def signMeUp():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserCreationForm()
    if request.method == "POST":
        print('POST request made')
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # add user to database
            user = User(username, email, password)

            # add instance to our db
            db.session.add(user)
            db.session.commit()
            flash("Successfully registered a new user", 'success')
            return redirect(url_for('auth.logMeIn'))
        else:
            flash('Invalid form. Please fill it out correctly.', 'danger')
    return render_template('signup.html', form = form)
