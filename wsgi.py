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

            data = trader.generate_features(ticker,start,end)
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
        box = request.form.get('Checkbox')
        
        if start and end:
            start = datetime.strptime(start,'%Y-%m-%d').strftime('%Y-%m-%d')
            end = datetime.strptime(end,'%Y-%m-%d').strftime('%Y-%m-%d')
            data = trader.simulate(tickers,start,end)

            if box:
                data = data[data['ACTION'] != 'HOLD']

            return render_template('results_simulate.html',data=data)
    return render_template('simulate.html')

@app.route('/learn/')
def learn():
    return render_template('learn.html')

if __name__ == '__main__':
    app.run(debug=True)
    