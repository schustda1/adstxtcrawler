#!/usr/bin/python
from dbconnect.backend import ConnectorFunctions
from sqlparse import format
from io import StringIO
import pandas as pd
import psycopg2
import datetime

class DADLConnector(ConnectorFunctions):

    def __init__(self, connection, verbose=0):
        super().__init__()
        self.verbose = verbose
        self._connect_to_database(self.credentials[connection])

    def _connect_to_database(self,connection):
        '''
        Function called when generating an instance of the class that
        opens the database connection.
        '''

        # print the connection string we will use to connect
        if self.verbose:
            print ("Connecting to database:".format(connection['dbname']))
            for k,v in connection.items():
                print ('   {0}  ->  {1}'.format(k,v))

    	# get a connection, if a connect cannot be made an exception will be raised here
        self.conn = psycopg2.connect(**connection)

    	# conn.cursor will return a cursor object, you can use this cursor to perform queries
        self.cursor = self.conn.cursor()

    def to_df(self,query_input,replacements={}):
        '''
        Takes in a string containing either a correctly formatted SQL
        query, or filepath directed to a .sql file. Returns a pandas DataFrame
        of the executed query.
        '''

        query = self._format_query(query_input,replacements)
        if self.verbose:
            print ('Executing Query:\n\n',format(query,reindent=True,keyword_case='upper'))
        return pd.read_sql(query,self.conn)

    def insert_into_table(self, df, table, type='append'):
        '''
        Inserts a pandas dataframe into the specified table in DADL.
        Types accepted are 'append' and 'replace'
        '''
        if len(table.split('.')) < 2:
            print ('Please specify a table schema')
            return
        if type == 'replace':
            truncate_query = 'TRUNCATE TABLE {0};'.format(table)
            self.cursor.execute(truncate_query)
            self.conn.commit()
            print ('\nTruncating table')

        insert_query = self._format_insert_statement(df,table)
        # print ('Inserting Data:\n\n',format(insert_query,reindent=True,keyword_case='upper'))
        self.cursor.execute(insert_query)
        self.conn.commit()

        # s_buf = StringIO()
        # df.to_csv(s_buf)
        # s_buf.seek(0)
        # self.cursor.copy_to(s_buf,table)
