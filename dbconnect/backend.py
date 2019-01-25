import json
import os
import datetime

class ConnectorFunctions(object):

    def __init__(self):
        self.load_credentials()

    def load_credentials(self):
        '''
        Loads the credentials stored in credentials.json to a dictionary
        variable called 'credentials'
        '''

        # if 'credentials.json' not in set(os.listdir("C:\Global Operations\DS\credentials\")):
        #     raise Exception('No credential file found!')

        with open('/Users/dschuster/Documents/Passwords/credentials.json') as f:
            self.credentials = json.loads(f.read())
            f.close()

    def _format_query(self,query_input,replacements={}):
        '''
        Takes in a string or .sql file and optional 'replacements' dictionary.

        Returns a string containing the formatted sql query and replaces the
        keys in the replacements dictionary with their values.
        '''

        # checks if input is a file or query
        if query_input.split('.')[-1] == 'sql':
            print('Reading .sql File')
            f = open(query_input,'r')
            f.close()
        else:
            query = query_input
        if replacements:
            for key,value in replacements.items():
                query = query.replace(key,str(value))
        return query

    def _format_insert_statement(self,df,table):
        '''
        Takes in a dataframe and table name (string).

        Returns SQL query with insert statement
        '''

        # Inserts require values to say Null instead of being empty
        df = df.fillna(value='Null')
        df = self._datetime_to_string(df)
        for col in df.columns:

            # adds formatting to string values
            try:
                df[col] = df[col].apply(lambda x: x.replace("'",''))
            except:
                pass
        insert_values = 'INSERT INTO {0} VALUES '.format(table)
        for idx, row in df.iterrows():
            insert_values += str(tuple(row.values)) + ','
        return insert_values[:-1].replace("'Null'","Null")

    def _datetime_to_string(self, df):
        '''
        Checks if any columns contain datetime values and converts them to
        strings. Needed when generating insert statments.
        '''

        datetime_columns = [num for num,value in enumerate(df.iloc[0].values) if isinstance(value,datetime.date)]
        for col in datetime_columns:
            df.iloc[:,col] = df.iloc[:,col].astype(str)
        return df


# if __name__ == '__main__':
    # c = ConnectorFunctions()
    # print (c.credentials['102'])
