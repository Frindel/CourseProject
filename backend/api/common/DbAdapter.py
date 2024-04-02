import psycopg2
from psycopg2 import sql
import threading
from bestconfig import Config

class DbAdapter:
    
    def __init__(self, prefix = None):
        self.__prefix = '' if prefix is None else prefix

        connection = self.__create_connection()
        connection.autocommit = True

        self.__cursor = connection.cursor()
        self.__connection = connection
        self.__lock = threading.Lock()

    def request(self, query):
        self.__lock.acquire()
        try:
            new_query = sql.SQL(query).format(sql.Identifier(self.__prefix))
            self.__cursor.execute(new_query)

            return self.__cursor.fetchall()
        finally:
            self.__lock.release()


    def __del__(self):
        self.__cursor.close()
        self.__connection.close()

    def __create_connection(self):
        config = Config()

        connection = psycopg2.connect(dbname=config["dbName"], 
                                      host=config["host"], 
                                      user=config["user"], 
                                      password=config["password"], 
                                      port=config["port"])
        return connection
