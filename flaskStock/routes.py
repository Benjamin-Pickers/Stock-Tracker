from flask import render_template, request, url_for, flash, redirect
from flaskStock import app, db
from flaskStock.webScrape import stockScraper
from flaskStock.forms import RegistrationForm, LoginForm
from flaskStock.model import User, StockData
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username =form.username.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Invalid Username, Try Again', 'danger')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        user = User(username=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, you can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    price_id = ""
    stocks = StockData.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        addItem = True
        symbol = request.form['symbol'].upper()
        scrape = stockScraper(symbol)
        info = scrape.get_info()

        #Check to see if change in price is negative, postive or none
        if '-' in info[2]:
            price_id = 'down'
        else:
            temp = info[2][0:3]
            if float(temp) > 0:
                price_id = 'up'

        #check if item is already in the database
        for item in stocks:
            if symbol in item.symbol:
                addItem = False
        if(addItem and info[0] != '0'):
            newStock = StockData(symbol= info[0], price = info[1], change = info[2], tracker= current_user)
            db.session.add(newStock)
            db.session.commit()
        elif (info[0] == '0'):
            flash('Not a valid TSX stock', 'danger')
        return redirect(url_for('home'))
    return render_template('home.html', stocks = stocks, price_id=price_id)


@app.route("/remove", methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        stocks = StockData.query.filter_by(user_id=current_user.id).all()
        for i in stocks:
            if (i.symbol == request.form['Remove']):
                db.session.delete(i)
                db.session.commit()
    return redirect(url_for('home'))

@app.route("/refresh", methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        stocks = StockData.query.filter_by(user_id=current_user.id).all()
        for info in stocks:
            scrape = stockScraper(info.symbol)
            newInfo = scrape.get_info()
            info.price = newInfo[1]
            info.change = newInfo[2]
            db.session.commit()
    return redirect(url_for('home'))
