import pandas as pd
import numpy as np

class Trading_Simulator:
    def __init__(self,cash,portfolio,watchlist,start_date,end_date):
        self.cash = cash
        self.folio = portfolio
        self.watchlist = watchlist
        self.start = start_date
        self.end = end_date

    def add_cash(self,amount):
        self.cash += amount

    def remove_cash(self,amount):
        self.cash -= amount

    def portfolio_add(self,stock):
        self.folio.append(stock)

    def portfolio_remove(self,stock):
        self.folio.remove(stock)

    def watchlist_add(self,stock):
        self.watchlist.append(stock)

    def watchlist_remove(self,stock):
        self.watchlist.remove(stock)

    def prepare_data(self):
        pass

    def simulate(self):
        pass