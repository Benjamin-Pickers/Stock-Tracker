from flask import render_template, request, url_for, flash, redirect
from flaskStock import app, db
from flaskStock.webScrape import stockScraper
from flaskStock.model import User, StockData


list = []

@app.route("/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['username']
        user = User(username=user_name)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, you can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        addItem = True
        priceId = ''
        symbol = request.form['symbol']
        scrape = stockScraper(symbol)
        info = scrape.get_info()

        #Check to see if change in price is negative, postive or none
        if '-' in info[2]:
            priceId = 'down'
        else:
            temp = info[2][0:3]
            if float(temp) > 0:
                priceId = 'up'
        info.append(priceId)

        #check if item is already in the list
        for item in list:
            if symbol in item:
                addItem = False
        if(addItem and info[0] != '0'):
            list.append(info)
        elif (info[0] == '0'):
            flash('Not a valid TSX stock', 'danger')
        return redirect(url_for('home'))
    return render_template('home.html', list = list)


@app.route("/remove", methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        for i in list:
            if (i[0] == request.form['Remove']):
                list.remove(i)
    return redirect(url_for('home'))

@app.route("/refresh", methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        for info in list:
            scrape = stockScraper(info[0])
            newInfo = scrape.get_info()
            info = newInfo
    return redirect(url_for('home'))
