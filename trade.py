import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import datetime,date

from utilities import *
from robinhood import *
from db import *

import matplotlib.pyplot as plt
path = r"C:\Users\zloef\db\trading.db"
client = Robinhood()
db = Database(path)
 
'''
Common trading strategies & ML algorithms for generating BUY/SELL signals
'''
class Trader:            
    def simulate(self,stocks,collection,start,end):
        s = stocks[0]
        dates = yf.download(s,start=start,end=end,period='2y').index
        dates = dates.to_pydatetime()

        results = pd.DataFrame(columns=['Date','Ticker','Price','RSI','Action'])
        i = 0
        for d in dates:
            d = d.strftime('%Y-%m-%d')

            for stock in stocks:
                try:
                    data = yf.download(stock,end=d,period='2y')
                    data = data.loc[:d,:]
                    
                    price = round(data['Adj Close'].iloc[-1],2)
                    rsi = relative_strength_index(data)
                    signal = rsi_signal(rsi)
                    action = 'HOLD'

                    if signal == 1:
                        action = 'BUY'
                    if signal == -1:
                        action = 'SELL'

                    db.update_trade_history((d,stock,price,rsi,action,collection)) 
                except:
                    print('Stock %s not found' % (stock))
                    stocks.remove(stock)

if __name__ == '__main__':
    trader = Trader()
    
    start = datetime(2020,8,3).strftime('%Y-%m-%d')
    end = datetime(2020,8,4).strftime('%Y-%m-%d')

    collections = ['finance','technology','oil-and-gas','software-service','energy','social-media','consumer-product','health']
    for col in collections:
        tickers = client.get_collection(col)
        trader.simulate(tickers,col,start,end)