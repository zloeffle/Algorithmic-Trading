import os
import requests
import random
import robin_stocks as rs
import yfinance as yf
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup


class Robinhood:
    username = None
    password = None
    auth_token = None
    refresh_token = None
    
    def __init__(self):
        self.device_token = self.GenerateDeviceToken() # generate device token upon initialization
        
    # generates a device token for the user
    def GenerateDeviceToken(self):
        rands = []
        for i in range(0,16):
            r = random.random()
            rand = 4294967296.0 * r
            rands.append((int(rand) >> ((3 & i) << 3)) & 255)

        hexa = []
        for i in range(0,256):
            hexa.append(str(hex(i+256)).lstrip("0x").rstrip("L")[1:])

        id = ""
        for i in range(0,16):
            id += hexa[rands[i]]
            if (i == 3) or (i == 5) or (i == 7) or (i == 9):
                id += "-"

        device_token = id
        return device_token

    '''
    Logs user into their robinhood account
    '''
    def login(self):
        username = input('Username: ')
        password = input('Password: ')
        self.username = username
        self.password = password
        
        # ensure that a device token has been generated
        if self.device_token == "":
                self.GenerateDeviceToken()

        # login via the robinhood api and update global authentication/refresh tokens
        login = rs.login(username, password)
        self.auth_token = login.get('access_token')
        self.refresh_token = login.get('refresh_token')
        return login
    
    # logs user out 
    def logout(self):
        logout = rs.logout()
        self.auth_token = None
        return logout
    
    '''
    Uses web scraping to retrieve a list of stocks from the specified robinhood collection
    '''
    def get_collection(self, collection):
        url = 'https://robinhood.com/collections/' + collection
        res = requests.get(url)
        data = res.text
        soup = BeautifulSoup(data)
        soup = soup.find('tbody')
        
        tickers = []
        for row in soup.findAll('tr'):
            i = 0
            for item in row.findAll('td'):
                if i > 1:
                    break
                temp = item.findAll('span')
                i += 1   
            tickers.append(temp[0].text)
        return tickers
        
if __name__ == '__main__':
    client = Robinhood()
    col = client.get_collection('software-service')
    