import psycopg2
from psycopg2 import sql
import threading
from bestconfig import Config

import sqlparse
from sqlparse.sql import Identifier, IdentifierList
from sqlparse.tokens import Keyword, Name


class DbAdapter:
    
    def __init__(self, prefix = None):
        self.__prefix = prefix

        connection = self.__create_connection()
        connection.autocommit = True

        self.__cursor = connection.cursor()
        self.__connection = connection
        self.__lock = threading.Lock()

    def request(self, script):
        self.__lock.acquire()
        try:
            formated_script = self.__addPrefixToScript(script, self.__prefix) if self.__prefix is not None else script

            request = sql.SQL(formated_script)
            self.__cursor.execute(request)

            return self.__cursor.fetchall() if self.__cursor.description else None
        finally:
            self.__lock.release()

    def __addPrefixToScript(self, script, suffix):
        # разбиение sql-скрипт на части
        parsed = sqlparse.parse(script)
        formatted_script = ""

        for statement in parsed:
            modified_statement = ""
            
            for token in statement.tokens:
                if isinstance(token, Identifier):
                    table_name = token.get_real_name()
                    new_table_name = f"{suffix}_{table_name}"
                    modified_statement += new_table_name
                else:
                    modified_statement += token.value

            formatted_script += modified_statement + ";"

        return formatted_script

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()

    def __create_connection(self):
        config = Config()

        connection = psycopg2.connect(dbname=config["dbSettings.dbName"], 
                                      host=config["dbSettings.host"], 
                                      user=config["dbSettings.user"], 
                                      password=config["dbSettings.password"], 
                                      port=config["dbSettings.port"])
        return connection
