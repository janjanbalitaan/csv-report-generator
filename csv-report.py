import os
import csv
import time
import json
import datetime
import base64

import pymysql
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId

def execute_query(cursor, query):
    try:
        cursor.execute(query)
        return cursor.description
        #return cursor.fetchall()
    except:
        return None

def get_db_cursor(connection):
    try:
        cur = connection.cursor()
        return cur
    except:
        return None

def get_db_connection(server_host, server_port, username, password, name):
    try:
        conn = pymysql.connect(host=server_host, port=server_port, user=username, passwd=password, db=name)
        return conn
    except:
        return None

if __name__ == '__main__':
    host = os.environ['DB_HOST']
    port = int(os.environ['DB_PORT'])
    name = os.environ['DB_NAME']
    user = os.environ['DB_USER']
    passwd = os.environ['DB_PASS']
    conn = get_db_connection(host, port, user, passwd, name)

    if conn is None:
        print('Cannot establish connection to the database')
    else:
        cur = get_db_cursor(conn)
        
        if cur is None:
            print('Cannot get database cursor')
        else:
            query = os.environ['DB_QUERY']
            desc = execute_query(cur, query)
            field_names = [i[0] for i in desc]
            data = cur.fetchall()
            timestr = time.strftime("%Y-%m-%d")
            pref = os.environ['FILE_PREF']
            dest = os.environ['FILE_DEST']
            filename = pref + timestr + '.csv' 
            filepath = dest + filename 
            with open(filepath, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                
                writer.writerow(field_names)
                for row in data:
                    writer.writerow(list(row))
                print("Wrote file to " + filepath)
            cur.close()         
            conn.close()
