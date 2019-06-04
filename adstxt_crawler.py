#!/usr/bin/env python

import sys
import csv
import json
import socket
import logging
from optparse import OptionParser
from urllib.parse import urlparse
import string
import urllib
import pyodbc
import requests
import sqlalchemy
import pandas as pd
from time import sleep

def generate_urls_file(filename, conn_string, list_num):

    query = '''
        SELECT domain FROM (
            SELECT domain, ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) % 8 r
            FROM reference.non_adstxt
        ) d
        WHERE r = {0}
    '''.format(list_num)

    engine = sqlalchemy.create_engine(conn_string,echo=False)
    df = pd.read_sql(query, engine)
    df.to_csv(filename, header=None, index=None)

#################################################################
# FUNCTION process_row_to_db.
#  handle one row and push to the DB
#
#################################################################

def process_row_to_db(conn, data_row, comment, hostname):
    insert_stmt = "INSERT INTO reference.adstxt (SITE_DOMAIN, EXCHANGE_DOMAIN, SELLER_ACCOUNT_ID, ACCOUNT_TYPE, TAG_ID, ENTRY_COMMENT) VALUES (?, ?, ?, ?, ?, ? );"
    exchange_host     = ''
    seller_account_id = ''
    account_type      = ''
    tag_id            = ''

    if len(data_row) >= 3:
        exchange_host = data_row[0].lower().strip()
        seller_account_id = data_row[1].lower().strip()
        account_type = data_row[2].lower().strip()

    if len(data_row) == 4:
        tag_id            = data_row[3].lower()

    #data validation heurstics
    data_valid = 1;

    # Minimum length of a domain name is 1 character, not including extensions.
    # Domain Name Rules - Nic AG
    # www.nic.ag/rules.htm
    if(len(hostname) < 3):
        data_valid = 0

    # knock out the bad characters
    if(len(exchange_host) < 3):
        data_valid = 0

    # could be single digit integers
    if(len(seller_account_id) < 1):
        data_valid = 0

    ## ads.txt supports 'DIRECT' and 'RESELLER'
    if(account_type not in ['direct','reseller']):
        data_valid = 0

    if(data_valid > 0):
        logging.debug( "%s | %s | %s | %s | %s | %s" % (hostname, exchange_host, seller_account_id, account_type, tag_id, comment))

        # Insert a row of data using bind variables (protect against sql injection)
        c = conn.cursor()
        try:
            c.execute(insert_stmt, (hostname, exchange_host, seller_account_id, account_type, tag_id, comment))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        # Save (commit) the changes
        return 1

    return 0

# end process_row_to_db  #####

#################################################################
# FUNCTION crawl_to_db.
#  crawl the URLs, parse the data, validate and dump to a DB
#
#################################################################

def crawl_to_db(conn, crawl_url_queue):

    rowcnt = 0

    myheaders = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36',
    #         'User-Agent': 'AdsTxtCrawler/1.0; +https://github.com/InteractiveAdvertisingBureau/adstxtcrawler',
            'Accept': 'text/plain',
        }
    printable = set(string.printable)
    urls = list(crawl_url_queue.keys())
    for num,aurl in enumerate(urls):
        try:
            print(num,aurl)
            ahost = crawl_url_queue[aurl]
            del crawl_url_queue[aurl]
            logging.info(" Crawling  %s : %s " % (aurl, ahost))
            r = requests.get(aurl, headers=myheaders,timeout=10)
            if(r.status_code == 200):
                tmpfile = 'tmpads.txt'

                # Check for redirects
                if 'ads.txt' not in r.url:
                    print('Not right for {0}'.format(aurl))
                    continue

                try:
                    with open(tmpfile, 'w') as tmp_csv_file:
                        corrected_text = filter(lambda x: x in printable, r.text)
                        corrected_text = ''.join(list(corrected_text))
                        tmp_csv_file.write(corrected_text)
                        tmp_csv_file.close()
                except:
                    pass

                with open(tmpfile, 'r', encoding = 'ascii') as tmp_csv_file:
                    #read the line, split on first comment and keep what is to the left (if any found)
                    line_reader = csv.reader(tmp_csv_file.read().splitlines(), delimiter='#', quotechar='|')
                    comment = ''

                    for line in line_reader:
                        # print(line)
                        logging.debug("DATA:  %s" % line)

                        try:
                            data_line = line[0]
                        except:
                            data_line = "";

                        #determine delimiter, conservative = do it per row
                        if data_line.find(",") != -1:
                            data_delimiter = ','
                        elif data_line.find("\t") != -1:
                            data_delimiter = '\t'
                        else:
                            data_delimiter = ' '

                        data_reader = csv.reader([data_line], delimiter=',', quotechar='|')
                        for row in data_reader:
                            if len(row) > 0 and row[0].startswith( '#' ):
                                continue
                            elif (len(line) > 1) and (len(line[1]) > 0):
                                comment = line[1]
                            domain_done = process_row_to_db(conn, row, comment, ahost)
                            if domain_done:
                                rowcnt += 1
                                break
                            # rowcnt = rowcnt + process_row_to_db(conn, row, comment, ahost)
                            # break
                        if domain_done:
                            break
                    domain_done = 0
                    # break
        except Exception as e:
            print (e)
            print('failed')
            pass
    return rowcnt

# end crawl_to_db  #####

#################################################################
# FUNCTION load_url_queue
#  Load the target set of URLs and reduce to an ads.txt domains queue
#
#################################################################

def load_url_queue(csvfilename, url_queue):
    cnt = 0
    with open(csvfilename, 'rt', encoding = 'ascii') as csvfile:
        targets_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in targets_reader:
            if len(row) < 1 or row[0].startswith( '#' ):
                continue

            for item in row:
                host = "localhost"

                if  "http:" in item or "https:" in item :
                    logging.info( "URL: %s" % item)
                    parsed_uri = urlparse(row[0])
                    host = parsed_uri.netloc
                else:
                    host = item
                    logging.info( "HOST: %s" % item)

            skip = 0

            try:
                #print "Checking DNS: %s" % host
                ip = socket.gethostbyname(host)

                if "127.0.0" in ip:
                    skip = 0 #swap to 1 to skip localhost testing
                elif "0.0.0.0" in ip:
                    skip = 1
                else:
                    logging.info("  Validated Host IP: %s" % ip)
            except:
                skip = 1

            if(skip < 1):
                ads_txt_url = 'http://{thehost}/ads.txt'.format(thehost=host)
                print(ads_txt_url)
                logging.info("  pushing %s" % ads_txt_url)
                url_queue[ads_txt_url] = host
                cnt = cnt + 1
    return cnt

# end load_url_queue  #####


#### MAIN ####
if __name__ == '__main__':

    list_num = sys.argv[1]

    with open('credentials.json') as credential_file:
        conn = json.load(credential_file)

    conn_string_pyodbc = 'DRIVER=' + '{' + 'ODBC Driver 17 for SQL Server' + '}' + ';PORT=1433;SERVER={server_name};DATABASE={database};UID={user};PWD={password}'.format(**conn)
    conn_string_sqlalchemy = "mssql+pyodbc:///?odbc_connect={}".format(urllib.parse.quote_plus(conn_string_pyodbc))

    # set status to running
    conn = pyodbc.connect(conn_string_pyodbc)
    cursor = conn.cursor()
    cursor.execute("UPDATE reference.adstxt_script SET isRunning = 1 WHERE process = 'adstxt{0}' ".format(list_num))
    conn.commit()
    conn.close()

    sleep(int(list_num) * 60)

    # start script
    crawl_url_queue = {}
    conn = None
    cnt_urls = 0
    cnt_records = 0

    filename = 'test.txt'
    generate_urls_file(filename, conn_string_sqlalchemy, list_num)
    cnt_urls = load_url_queue(filename, crawl_url_queue)

    conn = pyodbc.connect(conn_string_pyodbc)
    with conn:
        cnt_records = crawl_to_db(conn, crawl_url_queue)
        print(cnt_records)
        if(cnt_records > 0):
            conn.commit()

    print("Wrote {0} records from {1} URLs".format(cnt_records, cnt_urls))
    conn = pyodbc.connect(conn_string_pyodbc)
    cursor = conn.cursor()
    cursor.execute("UPDATE reference.adstxt_script SET isRunning = 0 WHERE process = 'adstxt{0}' ".format(list_num))
    conn.commit()
    conn.close()
