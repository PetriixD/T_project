#!/usr/bin/env python

from dotenv import load_dotenv
load_dotenv()
import os
from email_helpers import get_email_message, send_email
from utilities import get_monitoring_data, get_monitoring_data2, load_html
 
data = get_monitoring_data()
data2 = get_monitoring_data2()
html = load_html(data, data2)
msg = get_email_message('System status report', os.environ["FROM"], os.environ["TO"], html)
send_email(os.environ["FROM"], os.environ["PASS"], msg)
