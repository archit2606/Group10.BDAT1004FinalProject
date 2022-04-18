from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import requests
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta

app = Flask(__name__)

#setting up mongodb connection
client = MongoClient("mongodb+srv://archit:archit2606@cluster0.mxzq2.mongodb.net/BDAT1004?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.get_database('BDAT1004')
records = db.stocks

#getting data using API
url = "https://api.twelvedata.com/time_series?symbol=AAPL&interval=1day&apikey=demo&start_date=2022-01-01"
r = requests.get(url)
if r.status_code == 200:
    data = r.json()
    records.insert_one(data)

#loading the data into different lists which will be used to plot the graphs on the website
dates = []

for i in reversed(data["values"]):
    dates.append(i["datetime"])

closing_price = []

for i in reversed(data["values"]):
    closing_price.append(i["close"])

opening_price = []

for i in reversed(data["values"]):
    opening_price.append(i["open"])

high = []

for i in reversed(data["values"]):
    high.append(i["high"])

low = []

for i in reversed(data["values"]):
    low.append(i["low"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/openingprice")
def opening():
    date = dates
    values = opening_price
    return render_template('openingprice.html',labels = date, values = values)

@app.route("/closingprice")
def closing():
    date = dates
    values = closing_price
    return render_template('closingprice.html',labels = date, values = values)

@app.route("/highandlow")
def highandlow():
    date = dates
    value1 = high
    value2 = low
    return render_template('high.html',labels = date, value1 = high, value2 = low)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run()
