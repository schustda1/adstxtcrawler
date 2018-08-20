from oauth2client import client
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pandas.io.json.normalize import nested_to_record
from dbconnect.backend import ConnectorFunctions
import pandas as pd
import numpy as np

class DCMApi(ConnectorFunctions):

    def __init__(self, profileId=None, verbose=0):
        super().__init__()
        self.create_service()
        if not profileId:
            print ('Available profile ids listed below')
            self.get_user_ids()
        else:
            self.profileId = profileId
        self.verbose = verbose
        # self.profileId = 4553898

    def _get_list_columns(self,df):
        lst_columns = set()
        for row in df.iterrows():
            for num,value in enumerate(row[1]):
                if type(value) == list:
                    lst_columns.add(df.columns.tolist()[num])
        return lst_columns

    def create_service(self):
        API_SCOPES = ['https://www.googleapis.com/auth/dfareporting',
        'https://www.googleapis.com/auth/dfatrafficking',
        'https://www.googleapis.com/auth/ddmconversions']

        API_NAME = 'dfareporting'
        API_VERSION = 'v3.1'
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials['dcm'])
        self.service = build(API_NAME, API_VERSION, credentials=self.credentials)

    def _get_nested_columns(self,df,columns):
        nested_cols = {}
        for row in df.iterrows():
            for num,value in enumerate(row[1]):
                col = df.columns.tolist()[num]
                if col in columns:
                    pass
                elif type(value) == list:
                    nested_cols[col] = 'list'
                elif type(value) == dict:
                    nested_cols[col] = 'dict'
        return nested_cols

    def reduce_columns(self,df,columns):

        df_cols = set(df.columns.tolist())
        print ('\nCurrent Columns:', df_cols)
        columns_in_df = set()
        for col in columns:
            split_col = col.split('_')
            for i in range(len(split_col)):
                name = '_'.join(split_col[0:i+1])
                if name in df_cols:
                    columns_in_df.add(name)
        print('\nRemoving columns: ',df_cols-columns_in_df)
        return df[list(columns_in_df)]

    def splitDataFrameList(self, df,target_column,separator):
        ''' df = dataframe to split,
        target_column = the column containing the values to split
        separator = the symbol used to perform the split
        returns: a dataframe with each entry for the target column separated, with each element moved into a new row.
        The values in the other columns are duplicated across the newly divided rows.
        '''
        row_accumulator = []

        def splitListToRows(row, separator):
            split_row = row[target_column]
            try:
                for s in split_row:
                    new_row = row.to_dict()
                    new_row[target_column] = s
                    row_accumulator.append(new_row)
            except:
                split_row = [np.nan]
                for s in split_row:
                    new_row = row.to_dict()
                    new_row[target_column] = s
                    row_accumulator.append(new_row)

        df.apply(splitListToRows, axis=1, args = (separator, ))
        new_df = pd.DataFrame(row_accumulator)
        return new_df


    def unnest(self,df,columns):

        df = self.reduce_columns(df,columns)
        cols = self._get_nested_columns(df,columns)

        while len(cols) > 0:
            for col,typ in cols.items():
                if typ == 'list':
                    print('\nSplitting {0} into separate rows'.format(col))
                    df = self.splitDataFrameList(df,col,separator='_')
                elif typ == 'dict':
                    print('\nSplitting {0} into separate columns'.format(col))
                    df_new = df[col].apply(lambda x: {} if pd.isnull(x) else x)
                    df_new = df_new.apply(pd.Series)
                    df_new.columns = list(map(lambda x: str(col) + '_' + str(x), df_new.columns.tolist()))
                    df = pd.concat([df, df_new],axis=1).drop(columns=col)
            df = self.reduce_columns(df,columns)
            cols = self._get_nested_columns(df,columns)
        return df

    def list(self,obj,datatype,arguments={},fields=None,all=False,nested=True,
                key=None,value=None,columns=None,dropna=False):
        '''
        Calls the list method for the DCM Api. Arguments are as follows:
            - obj (string): The api object to pull from
            - datatype (string): Output datatype. Currently supported options
                are 'dict' and 'df' (dataframe)
            - arguments (dict): Any additional arguments to pass to the list method.
                (note: profileId is automatically added)
            - fields (list): Which fields to return
            - all (bool): Whether to make continuous api calls or just a single
            - nested (bool): Whether to leave object nested or unnest
            - key,value (string): if datatype is set to dict, specify the
                output key and values
            - columns (list): If datatype is set to df, reduce the
                dataframe to only return the specified columns
            - dropna (bool): Whether or not the dataframe can contain nulls
        '''


        arguments['profileId'] = self.profileId
        if self.verbose:
            print(arguments)
        request = eval('self.service.{0}().list(**arguments)'.format(obj))

        # Declare variables: 'first' is for creating dataframes, 'i' is num api
            # calls, output is for dictionaries
        first,i,dict_output,raw_output = True,0,{},[]

        while True:
            print('\nAPI Call Number {0}'.format(str(i+1)))
            response = request.execute()
            i += 1
            for x in response.keys():
                if x not in ['kind','nextPageToken']:
                    obj_name = x
                    break
            data = response[obj_name]
            # add the response entries to the current dictionary
            if datatype == 'dict':
                dict_output.update({str(i[key]).strip():str(i[value]).strip() for i in data})

            elif datatype == 'df':
                data = list(map(lambda x: nested_to_record(x,sep='_'),data))
                df_new = self.unnest(pd.DataFrame(data),columns)
                if dropna:
                    df_new = df_new.dropna()


                if first:
                    df_output,first = df_new,False
                else:
                    df_output = pd.concat([df_output,df_new],ignore_index=True)

            elif datatype == 'raw':
                raw_output.append(response)

            if not all:
                break
            elif response[obj_name] and response['nextPageToken']:
                request = eval('self.service.{0}().list_next(request, response)'.format(obj))
            else:
                break

        if self.verbose:
            print ('{0} api calls'.format(str(i)))

        if datatype == 'dict':
            return dict_output
        elif datatype == 'raw':
            return raw_output
        else:
            return df_output

    def get_user_ids(self):
        request = self.service.userProfiles().list()

        # Execute request and print response.
        response = request.execute()
        for profile in response['items']:
            print('Found user profile with ID %s and user name "%s".' %
            (profile['profileId'], profile['userName']))

if __name__ == '__main__':

    dcm = DCMApi(4553898)
    a = dcm.list('advertiserLandingPages',datatype='raw')

    # df = dcm.list(obj='creatives',datatype='dict',key='id',value='name')
