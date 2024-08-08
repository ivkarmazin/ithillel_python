from flask import Flask, request, jsonify, render_template_string
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

@app.route('/generate_users', methods=['GET'])
def generate_students():
    # count should be as input GET parameter
    count = int(request.args.get('count', 10))
    if not isinstance(count, int):
        return jsonify({'error': 'Input is not int'}), 400

    faker_instance = Faker("uk_UA")
    df = pd.DataFrame()
    # set limit as 1000
    for i in range(min(count, 1000)):
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
        <h1>Fake Users</h1>
        {table_html}
    </body>
    </html>
    """
    return html

@app.route('/bitcoin_rate', methods=['GET'])
def get_bitcoin_value():
    # /bitcoin_rate?currency=UAH&convert=100
    # input parameter currency code - default is USD
    # input parameter count and multiply by currency (int) - default count is 1
    currency = request.args.get('currency', 'USD')
    count = request.args.get('count', 1)

    # return value currency of bitcoin
    url = "https://test.bitpay.com/rates/BTC/" + currency

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-Accept-Version": "2.0.0"
    }

    response = requests.get(url, headers=headers)

    return str(float(json.loads(response.text)["data"]["rate"]) \
               * float(count))


if __name__ == '__main__':
    app.run(
        port=5000
        # , debug=True
    )