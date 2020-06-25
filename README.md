# csv-report-generator
Welcome to csv report generator. 

You may run csv generator to extract data from your mysql database table by using a query and also there is a script that you can send it to the email by using sendgrid

Requirements:
1. Python
2. Virualenv
3. Sendgrid client

How to run:
1. clone the repository
$ git clone https://github.com/janjanbalitaan/csv-report-generator.git
2. create a virtual environment in the project folder
$ virtualenv venv
3. create a report directory inside your project
$ mkdir reports
4. activate the virtual environment
$ source venv/bin/activate
5. install the requirements need
$ pip install -r requirements.txt
6. setup the environment files with .env extensions and modify depends on your available credentials
7. you may use the bash script for running or your may manually run it by doing the following:
* $ source venv/bin/activate
* $ source sample.env
* $ python csv-report.py
and it will automatically extract your csv report on the folder. The script with sendgrid functionalities will just send you an automated email

You may use it when your company is asking you to generate daily reports from mysql database and setup with cron jobs or you just want to extract csv file from a query in your mysql database

If you have questions or suggestions please email me at janjanbalitaan@gmail.com

Thank you for using it.
