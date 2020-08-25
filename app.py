from flask import Flask, render_template, redirect, request

from robinhood import *
from trade import *

import utilities
import random

app = Flask(__name__) 
client = Robinhood()

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
    