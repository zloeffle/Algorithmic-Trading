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
        stock = data[0]

        # BUYING STOCK
        if flag==1:
            # CHECK IF STOCK IS ALREADY OWNED
            self.cursor.execute('SELECT * FROM portfolio')
            rows = self.cursor.fetchall()
            
            temp = 0
            for row in rows:
                if stock in row:
                    temp = 1
                    break
            
            # if stock is already owned update the shares held, otherwise add it to portfolio
            if temp == 1:
                sql = ''' UPDATE portfolio SET shares=shares+1 WHERE ticker=? '''
                self.cursor.execute(sql,(stock,))
                self.conn.commit()
            else:
                sql = ''' INSERT INTO portfolio(ticker,price,shares,signal) VALUES(?,?,?,?) '''
                self.cursor.execute(sql,data)
                self.conn.commit()
        # SELLING STOCK
        else:
            # if only 1 share is held remove stock from portfolio, otherwise reduce shares held
            sql = ''' SELECT shares FROM portfolio WHERE ticker=? '''
            self.cursor.execute(sql,(stock,))
            res = self.cursor.fetchone()[0]

            print(res)
            if res <= 1:
                sql = 'DELETE FROM portfolio WHERE ticker=?'
                self.cursor.execute(sql,(stock,))
                self.conn.commit()
            else:
                sql = ''' UPDATE portfolio SET shares=shares-1 WHERE ticker=? '''
                self.cursor.execute(sql,(stock,))
                self.conn.commit()



    def delete_portfolio(self,data):
        sql = 'DELETE FROM portfolio WHERE ticker=?'
        self.cursor.execute(sql,(data,))
        self.conn.commit()

    def insert_trade_history(self,data):
        sql = ''' INSERT INTO trade_history(date,ticker,price,rsi,action)
                  VALUES(?,?,?,?,?) '''
        self.cursor.execute(sql,data)
        self.conn.commit()

if __name__ == '__main__':
    create_connection(r"C:\Users\zloef\db\algorithmic_trading.db")