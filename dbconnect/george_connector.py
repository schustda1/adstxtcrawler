#!/usr/bin/python
from dbconnect.backend import ConnectorFunctions
from sqlalchemy import create_engine
import pandas as pd

class GeorgeConnector(ConnectorFunctions):

    def __init__(self,connection,verbose=0):
        super().__init__()
        self.connection = connection
        self.verbose = verbose
        self.connect_to_george(self.credentials[self.connection])

    def connect_to_george(self,connection):
        print (connection)
        self.engine = create_engine(connection,client_encoding='utf8')
        self.conn = self.engine.connect()

    def to_df(self,query):
        return pd.read_sql(query,self.conn)

    def list_tables(self):
        table_query = '''SELECT CONCAT(table_schema,'.',table_name) AS table_name FROM information_schema.columns'''
        tables = self.to_df(table_query).table_name.unique()
        if self.verbose:
            for table in tables:
                print (table)
        tables.sort()
        return tables

    def list_columns(self,table=None):
        column_query = 'SELECT DISTINCT column_name FROM information_schema.columns'
        if table:
            column_query +=  'WHERE table_name = {0}'.format(talbe)
        columns = self.to_df(column_query).column_name.unique()
        if self.verbose:
            for column in columns:
                print (column)
        columns.sort()
        return columns


# if __name__ == '__main__':
#     george = GeorgeConnector('george1')
#     test_query = 'SELECT * FROM george.value'
#     # a = 'SELECT * FROM information_schema.columns'
#     df = george.to_df(test_query)
#     # cols = george.to_df(a)
#     tables = george.list_tables()
#     columns = george.list_columns()
