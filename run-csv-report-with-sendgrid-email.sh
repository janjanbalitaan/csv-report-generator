#!/bin/bash
cd <full path of the project>
source venv/bin/activate
source sample-with-sendgrid.env
python csv-report-with-sendgrid-email.py
