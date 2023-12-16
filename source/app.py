from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
import json

from api_work import get_crypto_rates

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_deals.db'
db = SQLAlchemy(app)

CRYPTO_RATES = {'BTC': 0, 'TON': 0, 'ETH': 0, 'USDT': 0, 'BNB': 0}

class CryptoDeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_rub = db.Column(db.Float, nullable=False)
    cryptocurrency = db.Column(db.String(50), nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    deal_type = db.Column(db.String(10), nullable=False)
    creating_time = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    deals = CryptoDeal.query.order_by(CryptoDeal.id.desc()).all()
    return render_template('index.html', deals=deals, crypto_rates=CRYPTO_RATES)

@app.route('/update_rates', methods=['POST'])
def update_rates():
    global CRYPTO_RATES
    btc_rate, ton_rate, eth_rate, usdt_rate, bnb_rate = get_crypto_rates()
    CRYPTO_RATES = {'BTC': btc_rate, 'TON': ton_rate, 'ETH': eth_rate, 'USDT': usdt_rate, 'BNB': bnb_rate}
    deals = CryptoDeal.query.order_by(CryptoDeal.id.desc()).all()
    return render_template('index.html', deals=deals, crypto_rates=CRYPTO_RATES)


@app.route('/add_deal', methods=['POST'])
def add_deal():
    amount_rub = request.form.get('amount_rub')
    cryptocurrency = request.form.get('cryptocurrency')
    exchange_rate = request.form.get('exchange_rate')
    deal_type = request.form.get('deal_type')
    creating_time = request.form.get('creating_time')

    if amount_rub and cryptocurrency and exchange_rate and deal_type and creating_time:
        # Преобразование строки в объект datetime
        creating_time = datetime.strptime(creating_time, '%Y-%m-%dT%H:%M')
        deal = CryptoDeal(amount_rub=amount_rub, cryptocurrency=cryptocurrency, exchange_rate=exchange_rate,
                          deal_type=deal_type, creating_time=creating_time)
        db.session.add(deal)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/filter_deals', methods=['POST'])
def filter_deals():
    start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%dT%H:%M')

    sales_sum = db.session.query(func.sum(CryptoDeal.amount_rub)).filter(
        CryptoDeal.deal_type == 'Продажа',
        CryptoDeal.creating_time.between(start_date, end_date)
    ).scalar() or 0

    purchase_sum = db.session.query(func.sum(CryptoDeal.amount_rub)).filter(
        CryptoDeal.deal_type == 'Покупка',
        CryptoDeal.creating_time.between(start_date, end_date)
    ).scalar() or 0

    difference = sales_sum - purchase_sum
    ratio = round(((sales_sum / purchase_sum - 1) * 100 - 0.5), 2) if purchase_sum != 0 else 0
    deals = CryptoDeal.query.order_by(CryptoDeal.id.desc()).all()

    return render_template('index.html', sales_sum=sales_sum, purchase_sum=purchase_sum, difference=difference, ratio=ratio, deals=deals, crypto_rates=CRYPTO_RATES)

if __name__ == '__main__':
    app.run(debug=True)
