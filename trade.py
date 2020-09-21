import os
from time import time
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import datetime,date,timedelta

from utilities import *
from robinhood import *
#from db import *

import matplotlib.pyplot as plt

'''
db = Database(path)
path = r"" 
'''
client = Robinhood()

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
    def generate_features(self,stock,start,end,short_ma=5,long_ma=25):
        # check that historical data for input stock can be found
        try:
            dates = yf.download(stock,start=start,end=end,period='2y').index
            dates = dates.to_pydatetime()
        except:
            print('%s not found' % stock)
            return None

        # download historical data and create the resultant dataframe
        data = yf.download(stock,end=end,period='2y').round(2)
        results = pd.DataFrame(columns=['PRICE','SHORT-MA','LONG-MA','BB-SIGNAL','RSI','TREND'],index=dates)
        
        # get price and signal features for each date
        for d in dates:
            price = data.loc[d,'Adj Close']

            # short and long simple moving averages
            short_sma = simple_moving_average(data,short_ma,d)
            long_sma = simple_moving_average(data,long_ma,d)
            
            # relative strength index
            rsi = relative_strength_index(data.loc[:d,:])

            # bollinger bands signal
            bb = bollinger_bands(data.loc[:d,:])
            bb_signal = bollinger_bands_signal(bb)

            # overall trend from the start date until the current date
            trend = trend_direction(data,d)
            
            # insert row into result dataframe
            results.loc[d,:] = [price,short_sma,long_sma,int(bb_signal),rsi,trend]

        results['DATE'] = results.index
        return results

    '''
    Simulate a trading scenario for a list of stocks over a specified date range

    Params
    - stocks: list of ticker symbols
    - start: start date
    - end: end date

    Returns
    - dataframe that shows the ticker, price, RSI score, recommended action, and profit from selling the stock on each respective date
    '''
    def simulate(self,stocks,start,end,short_ma,long_ma):
        portfolio = {}

        # initialize columns for result dataframe
        trade_history = pd.DataFrame(columns=['DATE','TICKER','PRICE','RSI','ACTION','PROFIT'])

        # get date range for simulation
        #dates = self.generate_features(stocks[0],start,end,short_ma,long_ma).index

        i = 0
        # generate feature data for each stock
        for stock in stocks:
            data = self.generate_features(stock,start,end,short_ma,long_ma)

            for date in data.index:
                # generate the approporiate action for each date from the signal features
                price = data.loc[date,'PRICE']
                short_ma = data.loc[date,'SHORT-MA']
                long_ma = data.loc[date,'LONG-MA']
                rsi = data.loc[date,'RSI']
                signal_bb = data.loc[date,'BB-SIGNAL']
                trend = data.loc[date,'TREND']
                action = self.signal(price,short_ma,long_ma,rsi,signal_bb,trend)
                profit = 0

                # BUY
                if action == 'BUY':
                    if stock not in portfolio:
                        portfolio[stock] = {'date':date,'price':data.loc[date,'PRICE'],'rsi':data.loc[date,'RSI']}

                # SELL
                if action == 'SELL':
                    if stock in portfolio:
                        profit = price - portfolio[stock]['price']
                        portfolio.pop(stock)
                
                # reformat date and insert row into result dataframe
                date = date.to_pydatetime().strftime('%Y-%m-%d')
                trade_history.loc[i,:] = [date,stock.upper(),price,data.loc[date,'RSI'],action,round(profit,2)]
                i += 1
        
        # compute total profit and sort rows by date
        profit = round(trade_history['PROFIT'].sum(),2)
        trade_history['DATE'] = pd.to_datetime(trade_history['DATE'])
        trade_history = trade_history.sort_values('DATE')
        return trade_history,profit

    def signal(self,price,short_ma,long_ma,rsi,bb_signal,trend):
        action = 'HOLD'

        # BUY
        if short_ma > long_ma:
            action = 'BUY'
        
        # SELL 
        if rsi > 85:
            action = 'SELL'
            
        return action

    def get_stocks_to_buy(self,collection,min_price,max_price,num_stocks,date):
        stocks = client.get_collection(collection)
        to_buy = {}
        temp = datetime.strptime(date,'%Y-%m-%d')
        temp = temp - timedelta(10)
        temp = datetime.strftime(temp,'%Y-%m-%d')
        
        for stock in stocks:
            try:
                data = yf.download(stock,period='2y')
            except:
                continue
            
            data = data.loc[:date,:].round(2)
            
            if data.empty:
                continue
            
            price = data['Adj Close'].iloc[-1]
            
            if price < min_price or price > max_price:
                continue
            
            short_ma = simple_moving_average(data,5,date)
            long_ma = simple_moving_average(data,25,date)
            rsi = relative_strength_index(data)     
            bb = bollinger_bands(data.loc[:date,:])
            bb_signal = bollinger_bands_signal(bb)
            trend = trend_direction(data,date)
            
            print(trend)
            break
            
            
        
                
                
if __name__ == '__main__':
    trader = Trader()
    client = Robinhood()
    start = datetime(2020,8,3).strftime('%Y-%m-%d')
    end = datetime(2020,8,4).strftime('%Y-%m-%d')
    data = yf.download('msft',period='2y')
    #data = data.loc[start:end,:]
    #print(data.iloc[0])
    #print(data)
    #t = trend_direction(data,start,end)
    trader.get_stocks_to_buy('technology',25,300,5,end)
    #start = datetime.strptime(start,'%Y-%m-%d')
    #print(start - timedelta(5))