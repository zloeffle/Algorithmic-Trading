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
        
    def generate_features(self,stock,start,end):
        data = yf.download(stock,period='2y') # retrieve 1 years worth of historical data from yahoo finance
        results = pd.DataFrame(index=data.loc[start:end].index) # set dates as index for result dataframe
        
        # add signal feature to result dataframe
        temp = data.loc[start:end,:] 
        
        
if __name__ == '__main__':
    trader = Trader()
    
    start = '2020-08-05'
    end = '2020-08-05'
    