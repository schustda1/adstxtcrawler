from dadl_connector import DADLConnector
import sys

if __name__ == '__main__':
    try:
        dadl = DADLConnector('pdw_gm',verbose=1)
    except:
        print ('Error in database conection')

    print ('\n connection successful \n')

    try:
        sample_query = 'SELECT advertiser_id FROM pdw_gm.pdw.dfa_std LIMIT 100;'
        df_string_test = dadl.to_df(sample_query)
        print ('to_df with string query works')
    except:
        print ('\n String test failed')
        e = sys.exc_info()[0]
        print( "<p>Error: %s</p>" % e )


    try:
        file_query = 'test/query_tester.sql'
        df_file_test = dadl.to_df(file_query)
        print ('to_df with file query works')
    except:
        print ('\n File test failed')
        e = sys.exc_info()[0]
        print( "<p>Error: %s</p>" % e )


    try:
        sample_query = 'SELECT advertiser_id FROM [Schema].dfa_std LIMIT 100;'
        replacements = {'[Schema]':'pdw'}
        df_file_test = dadl.to_df(sample_query,replacements)
    except:
        print ('\n File test failed')
        e = sys.exc_info()[0]
        print( "<p>Error: %s</p>" % e )
