#!/usr/bin/python
from dbconnect.backend import ConnectorFunctions
import pandas as pd
import pyodbc
import os
import json

class SSMSConnector(ConnectorFunctions):

    def __init__(self,server,verbose=0):
        ConnectorFunctions().__init__()
        self.load_credentials()

        self.verbose = verbose
        self.server = server
        self.connection = self.credentials[self.server]
        self.connect_to_database(self.connection)

    def load_credentials(self):
        '''
        Loads the credentials stored in credentials.json to a dictionary
        variable called 'credentials'
        '''

        if 'credentials.json' not in set(os.listdir('/Users/dschuster/Documents/Passwords/')):
            raise Exception('No credential file found!')

        with open('/Users/dschuster/Documents/Passwords/credentials.json') as f:
            self.credentials = json.loads(f.read())
            f.close()


    def connect_to_database(self,connection):
        # print the connection string we will use to connect

        if self.verbose:
            for x in connection.split(';'):
                print ('   {0}  ->  {1}'.format(x.split('=')[0],x.split('=')[1]))

    	# get a connection, if a connect cannot be made an exception will be raised here
        self.conn = pyodbc.connect(connection)

    	# conn.cursor will return a cursor object, you can use this cursor to perform queries
        self.cursor = self.conn.cursor()

        if self.verbose:
            print ("\nConnected!\n")

    def to_df(self,query,replacements={}):
        query = self._format_query(query,replacements)
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

# if __name__ == "__main__":
#     ssms = SSMSConnector('114',verbose=1)
    # query = "SELECT * FROM [vendors].[Chevy_LMA_New_Placements_Distribution_Table]"
    # df = ssms.to_df(query)
