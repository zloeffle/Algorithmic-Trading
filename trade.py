import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import datetime,date,timedelta

from utilities import *
#from db import *

import matplotlib.pyplot as plt

'''
db = Database(path)
path = r"" 
'''

class Trader:        
        
    '''
    Creates dataframe showing trading signals and price for a stock on each date in the specified range
    
    Params
    - stock: ticker for stock (string)
    - start: starting date for period (datetime)
    - end: ending date for period (datetime)
    
    Returns
    - pandas dataframe containing feature values for each date in specified range
    '''
    def generate_features(self,stock,start,end):
        # check that historical data for input stock can be found
        try:
            dates = yf.download(stock,start=start,end=end,period='2y').index
            dates = dates.to_pydatetime()
        except:
            print('%s not found' % stock)
            return None

        # download historical data and create the resultant dataframe
        data = yf.download(stock,end=end,period='1y').round(2)
        results = pd.DataFrame(columns=['PRICE','RSI','RSI-SIGNAL','BB-SIGNAL'],index=dates)
        
        # get price and signal features for each date
        for d in dates:
            price = data.loc[d,'Adj Close']
            
            rsi = relative_strength_index(data.loc[:d,:])
            rsi_sig = rsi_signal(rsi)

            bb = bollinger_bands(data.loc[:d,:])
            bb_signal = bollinger_bands_signal(bb)
    
            results.loc[d,:] = ['$'+str(price),rsi,rsi_sig,int(bb_signal)]

        results['DATE'] = results.index
        return results


    '''
    Gets stocks to buy/sell for each date in the given period based on values from the signal features
    
    Params
    - stocks: list of ticker strings
    - start: starting date for period (datetime)
    - end: ending date for period (datetime)
    
    Returns
    - tuple containing 2 dictionaries for stocks that should be bought/sold (key: ticker values: date,price,signal features)
    '''
    def get_stocks(self,stocks,start,end):
        # initialize dictionaries to return
        to_buy = {}
        to_sell = {}

        # generate features for each stock
        for stock in stocks:
            data = self.generate_features(stock,start,end)
            
            # check that feature data is not null
            if data is not None:
                
                # generate action for each date in feature data
                for date in data.index:
                    rsi = data.loc[date,'RSI-SIGNAL']
                    bb = data.loc[date,'BB-SIGNAL']

                    # BUY
                    if rsi == 1 and bb == 1:
                        if stock not in to_buy:
                            date = date.to_pydatetime().strftime('%Y-%m-%d')
                            to_buy[stock] = {'date':date,'price':data.loc[date,'PRICE'],'rsi':data.loc[date,'RSI']}
                    # SELL
                    if rsi == -1 and bb == -1:
                        if stock in to_buy:
                            date = date.to_pydatetime().strftime('%Y-%m-%d')
                            to_sell[stock] = {'date':date,'price':data.loc[date,'PRICE'],'rsi':data.loc[date,'RSI']}
                            
        return to_buy,to_sell

    '''
    Simulate a trading scenario for a list of stocks over a specified date range

    Params
    - stocks: list of ticker symbols
    - start: start date
    - end: end date

    Returns
    - dataframe that shows the ticker, price, RSI score, recommended action, and profit from selling the stock on each respective date
    '''
    def simulate(self,stocks,start,end):
        portfolio = {}
        portfolio_value = 0

        # initialize columns for result dataframe
        trade_history = pd.DataFrame(columns=['DATE','TICKER','PRICE','RSI','ACTION','PROFIT'])

        # seperate stocks that generate buy/sell signals at anypoint during the specified date range
        to_buy,to_sell = self.get_stocks(stocks,start,end)

        i = 0
        # traverse buy/sell groups and populate result dataframe with trade records 
        for stock in to_buy:
            data = to_buy[stock]
            portfolio[stock] = data
            portfolio_value += data['price']
            trade_history.loc[i,:] = [data['date'],stock.upper(),'$'+str(data['price']),data['rsi'],'BUY','$'+str(0)]                
            i += 1
            
        for stock in to_sell:
            data = to_sell[stock]
            portfolio_value -= portfolio[stock]['price']
            portfolio.pop(stock)
            profit = data['price']-to_buy[stock]['price']
            trade_history.loc[i,:] = [data['date'],stock.upper(),'$'+str(data['price']),data['rsi'],'SELL','$' + str(round(profit,2))]
            i += 1

        # convert date column to datetime type and sort records by date
        trade_history['DATE'] = pd.to_datetime(trade_history['DATE'])
        trade_history = trade_history.sort_values('DATE')
        return trade_history.round(2)

if __name__ == '__main__':
    trader = Trader()
    
    start = datetime(2020,8,1).strftime('%Y-%m-%d')
    end = datetime(2020,8,14).strftime('%Y-%m-%d')
    