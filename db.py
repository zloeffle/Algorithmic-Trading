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
