from flask import Flask
import random
import string
import pandas as pd

app = Flask(__name__)

@app.route("/admin")
def hello_world():
    return "<p>Hello— Vanya</p>"


@app.route("/generate_password")
def generate_password(length=None):
    if length is None:
        length = random.randint(10, 20)

    length = max(10, min(length, 20))
    characters = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


@app.route("/calculate_average")
def calculate_average():
    # csv file with students     1.calculate average high     2.calculate average weight
    df = pd.read_csv("hw.csv")
    return(str(df[" Height(Inches)"].mean()) + "  " + str(df[" Weight(Pounds)"].mean()))


if __name__ == '__main__':
    app.run(
        port=5000, debug=True
    )