from flaskStock import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    data = db.relationship('StockData', backref='tracker', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

class StockData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(25), unique=True, nullable=False)
    price = db.Column(db.String(25), nullable=False)
    change = db.Column(db.String(15), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"StockData('{self.symbol}', '{self.price}', '{self.change}')"
