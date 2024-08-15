from flask import Flask, request, jsonify, render_template_string
from webargs import fields
from webargs.flaskparser import use_args
from faker import Faker
import random
from datetime import datetime, timedelta
import pandas as pd
import requests
import json

app = Flask(__name__)
def random_birthday():
    start= datetime.strptime('1964-01-01', '%Y-%m-%d')
    end = datetime.strptime('2006-12-31', '%Y-%m-%d')
    return start + timedelta(days=random.randint(0, int((end - start).days)))

user_args_pass = {
'count': fields.Int(missing=10, default=10)
    }

@app.route('/generate_users', methods=['GET'])
@use_args(user_args_pass, location="query")
def generate_students(args):
    # count should be as input GET parameter
    count = args['count']
    if not isinstance(count, int):
        return jsonify({'error': 'Input is not int'}), 400

    faker_instance = Faker("uk_UA")
    df = pd.DataFrame()
    # set limit as 1000
    warning = ''
    if count > 1000:
        warning = ' (Max 1000 count)'
        count = min(count, 1000)
    for i in range(count):
        # first_name, last_name, email, password, birthday (18-60)
        new_row = {
            'name': faker_instance.first_name(),
            'last_name': faker_instance.last_name(),
            'email': faker_instance.email(),
            'password': faker_instance.password(),
            'birthday': random_birthday().strftime('%Y-%m-%d')
            }
        df = df._append(new_row, ignore_index=True)

    # save to csv and show on web page
    file = 'users.csv'
    df.to_csv(file, index=False)
    table_html = df.to_html(index=False)

    html = f"""
    <html>
    <head><title>Fake Users</title></head>
    <body>
        <h1>Fake Users{warning}</h1>
        {table_html}
    </body>
    </html>
    """
    return html

user_args_btc = {
    'currency': fields.Str(missing='USD', default='USD'),  # Required int, must be > 0
    'count': fields.Str(missing='1', default='1')  # Optional string, defaults to 'User'
}

@app.route('/bitcoin_rate', methods=['GET'])
@use_args(user_args_btc, location="query")
def get_bitcoin_value(args):
    # /bitcoin_rate?currency=UAH&convert=100
    # input parameter currency code - default is USD
    # input parameter count and multiply by currency (int) - default count is 1
    currency = args['currency']
    count = args['count']

    # return value currency of bitcoin
    url = "https://test.bitpay.com/rates/BTC/" + currency

    response = requests.get(url)
    if response.status_code == 200:
        price = json.loads(response.text)["data"]["rate"]
        price = float(price)
        count = float(count)
        return str(price * count)


if __name__ == '__main__':
    app.run(
        port=5000
        # , debug=True
    )