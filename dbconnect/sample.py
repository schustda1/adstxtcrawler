from DBConnectors.bigquery_connector import BigQueryConnector
from DBConnectors.dadl_connector import DADLConnector
from DBConnectors.george_connector import GeorgeConnector
from DBConnectors.ssms_connector import SSMSConnector



if __name__ == '__main__':

    dbs = ['BigQuery','DADL','George','SSMS']
    connection_options = ''
    for num,db in enumerate(dbs):
        connection_options += '\n{0}. {1}'.format(num+1,db)

    choice = int(input("Which database would you like to connect to? {0}\n\n".format(connection_options)))

    if choice == 1:
        name = input("\nWhich Dataset would you like to connect to?  ".format(dbs[choice-1]))
    else:
        name = input("\nWhat is the key for {0}?  ".format(dbs[choice-1]))


    if choice == 1:
        bq = BigQueryConnector(name)
        sample_query = 'SELECT * FROM `DCM_GMNA.activity_8334` LIMIT 100'
        print('Running sample query: {0}'.format(sample_query))
        df = bq.to_df(sample_query)
        print('Success, query results loaded to variable df')
    if choice == 2:
        dadl = DADLConnector(name)
        sample_query = 'SELECT * FROM pdw_gm.carat_gm.dcm_date LIMIT 100'
        print('Running sample query: {0}'.format(sample_query))
        df = dadl.to_df(sample_query)
        print('Success, query results loaded to variable df')
