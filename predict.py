import os
import pandas as pd
import numpy as np
import math
import random
from datetime import date

from utilities import *
from robinhood import *
from perceptron import *
from LinearRegression import *
from KNN import *
from DecisionTree import * 

import matplotlib.pyplot as plt

client = Robinhood()
        
'''
Common trading strategies & ML algorithms that generate buy signals and predict a stocks return 14days ahead
'''
class Signal:
    def __init__(self,data):
        self.portfolio = data
        self.results = {}           
    
    '''
    Generate features using indicators from utilities.py
    '''
    def create_features(self,data,end_date='2020-05-29',future_date='2020-06-05'):
        df = self.portfolio
        
        for t in list(df.index):
            # historical data
            hist = client.get_historicals(t)
            
            # past and future prices
            try:
                past_price = hist.loc[end_date,'Adj Close']
                future_price = hist.loc[future_date,'Adj Close']
            except KeyError:
                continue
                
            # signals
            sma = simple_moving_average(hist,end_date) # simple MA 
            ma = moving_average(hist,end_date) # MA
            mac = macd(hist,end_date) # MACD
            rsi = relative_strength_index(hist,end_date) # RSI
            
            # add features for each stock
            df.loc[t,'Simple MA'] = sma
            df.loc[t,'MA'] = ma
            df.loc[t,'MACD'] = mac
            df.loc[t,'RSI'] = rsi
            df.loc[t,'7-Day Profit']  = future_price > past_price

        df.dropna(inplace=True,axis=0)
        return df

    '''
    Implementation of Multiple Linear Regression
    
    Features: Open, High, Low, Volume, Adj Close
    Predictors: Open, High, Low, Volume
    Target: Adj Close
    '''
    def linear_regression(self,data):
        model = LinearRegression()
        features = list(data.columns)
        
        x = data[['Open','High','Low','Volume']]
        y = data['Adj Close']
        
        split = '2020-05-29'
        x_train,y_train,x_test,y_test = model.train_test_split(x,y,split)
        x_test = x_test.iloc[1:]
        y_test = y_test.iloc[1:]
        
        model.fit(x_train.to_numpy(),y_train.to_numpy())
        preds = model.predict(x_test.to_numpy(),y_test.to_numpy())
        
        x_test['Actual Price'] = y_test
        x_test['Predicted Price'] = preds
        return x_test
        
    def knn_classifier(self,data):
        model = KNN(10)
        data.set_index('Ticker',inplace=True)
        
        train = data.iloc[:-5]
        test = data.iloc[-5:]
        validation = test['7-Day Profit']
        test.drop('7-Day Profit',axis=1,inplace=True)
        test = test.to_numpy()
        
        classifications = []
        for row in test:
            neighbors = model.get_neightbors(train,row)
            classifications.append(model.classify(neighbors))
        
        result = pd.DataFrame(test,index=data.iloc[-5:].index,columns=['Simple MA','MA','MACD','RSi'])
        result['Actual Signal'] = data['7-Day Profit'].iloc[-5:]
        result['Predicted Signal'] = classifications
        return result
        
    def decision_tree(self,data):
        model = DecisionTree()
        data.set_index('Ticker',inplace=True)
        data['7-Day Profit'] = data['7-Day Profit'].astype(int)
        
        tree = model.build_tree(data,1)
        model.print(tree,10)

    def multilayer_perceptron(self,data):
        pass
        
if __name__ == '__main__':
    df1 = pd.read_csv('train_04-30-2020.csv')
    df2 = pd.read_csv('train_05-29-2020.csv')
    df3 = pd.read_csv('train_06-01-2020.csv')
    s = Signal(df1)
    
    # Linear Regression
    stocks = ['UAL','BAC','AMD']
    df = client.get_historicals(stocks[0])
    res = s.linear_regression(df)
    
    # Decision Tree
    s.decision_tree(df1)
    
    # KNN
    
    
    # MLP
        