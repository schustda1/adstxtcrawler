### DBConnectors

***Still in Development***


Personal repository to aid in ETL and data exploration.

Database credentials to be stored in a .json file called 'credentials.json'

* For BigQuery, key should be named `'bigquery'` and the value should contain a string with the directory location
of a service account .json file
* For DADL and George, the key will be whatever name you would like to call (I use the database name, i.e. `pdw_gm`), the value should be a dictionary containing the following keys
  * 'dbname'
  * 'user'
  * 'password'
  * 'host'
For more info, see http://initd.org/psycopg/docs/module.html
* For SSMS, the key can be what ever name you want, an the value is the following connection info (do not change the {SQL Server} portion):

`"Driver={SQL SERVER};SERVER=[Insert Server];DATABASE=[Insert DB];UID=[Insert User ID];PWD=[Insert Password]"`

Run `sample.py` to test if your connections are successful
