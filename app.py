from flask import Flask, render_template, redirect, request

from robinhood import *
from trade import *

import utilities
import random

app = Flask(__name__) 
client = Robinhood()
trader = Trader()

@app.route('/',methods=['GET','POST'])
def index():
    #if request.method == 'GET':

    ticker = request.form.get('Ticker')
    start = request.form.get('StartDate')
    end = request.form.get('EndDate')
    print(ticker,start,end)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    