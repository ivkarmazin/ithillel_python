from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args
import sqlite3
from datetime import timedelta

def execute_query(query, args=()):
    with sqlite3.connect('chinook.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query, args)
        connection.commit()
        records = cursor.fetchall()
    return records
app = Flask(__name__)

user_args_country = {
    'country': fields.Str(missing='ALL', dump_default='ALL')
    }
@app.route('/country-revenue', methods=['GET'])
@use_args(user_args_country, location="query")
def country_revenue(args):
    country = args['country']
    if country != 'ALL':
        query = "SELECT SUM(TOTAL) FROM invoices WHERE BillingCountry = '{}'".format(country)
        data = execute_query(query=query)
    else:
        query = "SELECT SUM(TOTAL) FROM invoices"
        data = execute_query(query=query)
    return data

@app.route('/total-time')
def total_time():
    query = "SELECT SUM(Milliseconds) FROM tracks"
    time = execute_query(query=query)
    time = time[0][0]
    time = timedelta(milliseconds = time)
    return str(time)

if __name__ == '__main__':
    app.run(
        port=5000
        # , debug=True
    )