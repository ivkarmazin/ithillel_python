from flask import Flask
from webargs import fields
from webargs.flaskparser import use_kwargs
from db_handler import execute_query
app = Flask(__name__)

user_args_city = {
    'city': fields.Str(missing='Madrid', dump_default='Madrid')
    }
@app.route('/city-genre', methods=['GET'])
@use_kwargs(user_args_city, location="query")
def city_genre(city):

    query = ("SELECT g.Name \
                FROM genres g \
                JOIN tracks t ON t.GenreId = g.GenreId \
                JOIN invoice_items ii ON ii.TrackId = t.TrackId \
                JOIN invoices i ON i.InvoiceId = ii.InvoiceId \
                WHERE i.BillingCity = '{}' \
                GROUP BY i.BillingCity, g.Name \
                ORDER BY COUNT(g.Name) DESC \
                LIMIT 1;").format(city)
    data = execute_query(query=query)

    return data

if __name__ == '__main__':
    app.run(
        port=5000
        # , debug=True
    )