from flask import Flask, render_template, redirect, request

from robinhood import *
from trade import *

import utilities
import random
from datetime import datetime
import pandas as pd

app = Flask(__name__) 
client = Robinhood()
trader = Trader()

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # get form data
        ticker = request.form.get('Ticker')
        start = request.form.get('StartDate')
        end = request.form.get('EndDate')

        # check that form data is not null
        if ticker and start and end:
            start = datetime.strptime(start,'%Y-%m-%d').strftime('%Y-%m-%d')
            end = datetime.strptime(end,'%Y-%m-%d').strftime('%Y-%m-%d')

            data = trader.generate_features(ticker,start,end)
            data['DATE'] = pd.to_datetime(data['DATE'],format='%Y-%m-%d')
            
            return render_template('results.html',data=data,stock=ticker)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    