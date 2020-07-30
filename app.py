from flask import Flask, render_template, redirect, request
from robinhood import *
from trade import *
import utilities
import random

app = Flask(__name__) 
client = Robinhood()

@app.route('/', methods=['GET', 'POST'])
def login():
    pass

@app.route('/logout')
def logout():
    user.logout()
    return redirect('/')

''' 
Homepage displaying a users current holdings, watchlist, and buy/sell functionality
Watchlist and portfolio also includes buy/sell recomendations for each stock
'''
@app.route('/home', methods=['GET', 'POST'])
def home():
    pass

if __name__ == '__main__':
    app.run(port=5000)
    