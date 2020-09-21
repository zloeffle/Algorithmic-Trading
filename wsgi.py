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

@app.route('/simulate/',methods=['GET','POST'])
def simulate():
    if request.method == 'POST':
        # get form data
        tickers = request.form.get('Tickers').split(',')
        start = request.form.get('StartDate')
        end = request.form.get('EndDate')
        short_ma = int(request.form.get('ShortMA'))
        long_ma = int(request.form.get('LongMA'))
        box = request.form.get('Checkbox')
        
        if start and end:
            start = datetime.strptime(start,'%Y-%m-%d').strftime('%Y-%m-%d')
            end = datetime.strptime(end,'%Y-%m-%d').strftime('%Y-%m-%d')
            data,profit = trader.simulate(tickers,start,end,short_ma,long_ma)

            if box:
                data = data[data['ACTION'] != 'HOLD']

            return render_template('results_simulate.html',data=data,profit=profit)
    return render_template('simulate.html')

    @app.route('/buy_stocks/',methods=['GET','POST'])
    def buy_stocks():
        if request.method == 'POST':
            return render_template('buy_stocks.html')
        return render_template('buy_stocks.html')
        
    

if __name__ == '__main__':
    app.run(debug=True)
    