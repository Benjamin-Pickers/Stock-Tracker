from flask import render_template, request, url_for, flash, redirect, Blueprint
from flaskStock import db
from flaskStock.users.forms import RegistrationForm, LoginForm
from flaskStock.model import User
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)


@users.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('stocks.home'))
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username =form.username.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('stocks.home'))
        else:
            flash('Invalid Username, Try Again', 'danger')
    return render_template('login.html')

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        user = User(username=form.username.data)
        available = User.query.filter_by(username =form.username.data).first()
        if available:
            flash('Username is already taken, please chose another', 'danger')
            return redirect(url_for('users.register'))
        else:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created, you can now login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html')
