#!/usr/bin/python
from dbconnect.backend import ConnectorFunctions
from google.cloud import bigquery
import pandas as pd
import os
import json

class BigQueryConnector(ConnectorFunctions):
    def __init__(self,project_dataset):
        ConnectorFunctions().__init__()
        self.load_credentials()

        self.project_id = 'us-gm-175021'
        self.project_dataset = project_dataset
        self.dataset_ref = bigquery.DatasetReference(self.project_id,self.project_dataset)
        self.private_key = self.credentials['bigquery']
        self.client = bigquery.Client.from_service_account_json(self.private_key)
        self.tables = [table.table_id for table in self.client.list_tables(self.dataset_ref)]

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

    def create_view(self,view_name,query,overwrite=True,replacements={}):
        '''
        Creates a view given a query
        '''

        if overwrite and view_name in self.tables:
            table_ref = self.dataset_ref.table(view_name)
            self.client.delete_table(table_ref)

        table = bigquery.Table(table_ref)
        table.view_query = self._format_query(query,replacements)
        table.view_use_legacy_sql = False
        self.client.create_table(table)
        print ('{0} view created'.format(view_name))

    def delete_table(table_id, project=None):
        """
        Deletes a table in a given dataset.
        """
        bigquery_client = self.Client(project=project)
        dataset_ref = self.Client.dataset(self.dataset_id)
        table_ref = dataset_ref.table(table_id)
        bigquery_client.delete_table(table_ref)
        print('Table {0}:{1} deleted.'.format(dataset_id, table_id))

    def to_bq(self,df,table_name):
        '''
        Export a pandas dataframe to Google BigQuery saved as the table name
        '''
        dest = self.project_dataset + "." + table_name
        df.to_gbq(destination_table=dest,project_id=self.project_id, private_key=self.private_key)

    def to_df(self,query,replacements={}):
        '''
        Executes the input query and returns the result as a pandas dataframe
        '''
        # print ('Querying Table')
        # query_job = self.client.query(query)
        # print ('Querying Complete. Converting to DataFrame...')
        # return query_job.to_dataframe()

        query = self._format_query(query,replacements)
        return pd.read_gbq(query,project_id=self.project_id,private_key=self.private_key,dialect='standard')


# if __name__ == '__main__':
#     bq = BigQueryConnector('DCM_GMNA')
#     df = bq.to_df('test/bigquery_sql_file.sql')
#     bq.to_bq(df,'test')
    # bq.list_tables()
    # query = '''SELECT * FROM `us-gm-175021.DCM_GMNA.activity_8334` LIMIT 1000'''
    # df = bq.to_df(query)
