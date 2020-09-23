from flask import Flask, render_template, redirect, request

from trade import *
import utilities

import random
from datetime import datetime
import pandas as pd

'''
Web Server Gateway Interface
'''
app = Flask(__name__) 
trader = Trader()

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # get form data
        ticker = request.form.get('Ticker').upper()
        start = request.form.get('StartDate')
        end = request.form.get('EndDate')

        # check that form data is not null
        if ticker and start and end:
            start = datetime.strptime(start,'%Y-%m-%d').strftime('%Y-%m-%d')
            end = datetime.strptime(end,'%Y-%m-%d').strftime('%Y-%m-%d')
            short_ma = int(request.form.get('ShortMA'))
            long_ma = int(request.form.get('LongMA'))

            data = trader.generate_features(ticker,start,end,short_ma,long_ma)
            data['DATE'] = pd.to_datetime(data['DATE'],format='%Y-%m-%d')
            
            return render_template('results_analyze.html',data=data,stock=ticker)
    return render_template('index.html')

@app.route('/buy/',methods=['GET','POST'])
def buy():
    if request.method == 'POST':
        col = request.form.get('Collection')
        min_price = float(request.form.get('min_price'))
        max_price = float(request.form.get('max_price'))
        date = request.form.get('date')
        print(col,min_price,max_price,date)

        if col and min_price and max_price and date:
            data = trader.get_stocks_to_buy(col,min_price,max_price,date)
            return render_template('results_buy.html',data=data)
    return render_template('buy.html')

if __name__ == '__main__':
    app.run(debug=True)
    