import os
import csv
import time
import json
import datetime
import base64

import pymysql
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId

def send_email(sendgrid_client, message):
    try:
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        print('Successful sending of email')
    except Exception as e:
        print(e.message)

def get_sendgrid_client(api_key):
    try:
        sendgrid_client = SendGridAPIClient(api_key)

        return sendgrid_client
    except:
        return None

def set_email_message(senders, recipients, subject, content):
    try:
        message = Mail(
                from_email=senders,
                to_emails=recipients,
                subject=subject,
                html_content=content
                )
        return message
    except:
        return None

def set_email_attachment(filename, encoded):
    try:
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType('text/csv')
        attachment.file_name = FileName(filename)
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId(filename)

        return attachment
    except:
        return None

def get_encoded_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            f.close()
        
        encoded = base64.b64encode(data).decode()

        return encoded
    except:
        return None

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

            encoded = get_encoded_file(filepath)
            
            if encoded is None:
                print('Can\'t encode the file')
            else:
                attachment = set_email_attachment(filename, encoded) 

                email_to = os.environ['EMAIL_TO']
                email_from = os.environ['EMAIL_FROM']
                email_subject = os.environ['EMAIL_SUBJECT'] + ' (' + timestr + ')'
                email_content = os.environ['EMAIL_CONTENT']
                
                senders = email_from#.split(';')
                recipients = email_to#.split(';')
                message = set_email_message(senders, recipients, email_subject, email_content)
                
                email_key = os.environ['EMAIL_KEY']
                sendgrid_client = get_sendgrid_client(email_key)

                if sendgrid_client is None:
                    print('Can\'t create a sendgrid client')
                else:
                   send_email(sendgrid_client, message) 
