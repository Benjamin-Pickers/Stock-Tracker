from flask import render_template, request, url_for, flash, redirect, Blueprint
from flaskStock import db
from flaskStock.webScrape import stockScraper
from flaskStock.model import User, StockData
from flask_login import login_user, current_user, logout_user, login_required

stocks = Blueprint('stocks', __name__)

@stocks.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    stocks = StockData.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        addItem = True
        symbol = request.form['symbol'].upper()
        scrape = stockScraper(symbol)
        info = scrape.get_info()

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
        return redirect(url_for('stocks.home'))
    return render_template('home.html', stocks = stocks)


@stocks.route("/remove", methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        stocks = StockData.query.filter_by(user_id=current_user.id).all()
        for i in stocks:
            if (i.symbol == request.form['Remove']):
                db.session.delete(i)
                db.session.commit()
    return redirect(url_for('stocks.home'))

@stocks.route("/refresh", methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        stocks = StockData.query.filter_by(user_id=current_user.id).all()
        for info in stocks:
            scrape = stockScraper(info.symbol)
            newInfo = scrape.get_info()
            info.price = newInfo[1]
            info.change = newInfo[2]
            db.session.commit()
    return redirect(url_for('stocks.home'))
