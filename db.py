import sqlite3 as sql
from sqlite3 import Error

class Database:
    def __init__(self,path):
        self.conn = self.create_connection(path)
        self.cursor = self.conn.cursor()

    def create_connection(self,db_file):
        conn = None
        try:
            conn = sql.connect(db_file)
            print(sql.version)
        except Error as e:
            print(e)

        return conn

    def update_portfolio(self,data,flag=0):
        sql = ''' INSERT INTO portfolio(ticker,shares) VALUES(?,?) '''

    def update_trade_history(self,data):
        sql = ''' INSERT INTO trade_history(date,ticker,price,rsi,action,collection) VALUES(?,?,?,?,?,?) '''
        self.cursor.execute(sql,data)
        self.conn.commit()