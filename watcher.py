import os
from tabulate import tabulate
import psutil
import smtplib
from email.mime.text import MIMEText

disk_usage = os.popen("df --output=avail -m / | awk 'NR==2 {print $1}'").read().strip()

process_count = os.popen("ps -A | wc -l").read().strip()

cpu_util = psutil.cpu_percent()

ram = psutil.virtual_memory()
ram_util = ram.percent

current_users_count = os.popen("who | wc -l").read().strip()

who_output = os.popen('who').read().strip()
user_lines = who_output.split('\n')
user_columns = ", ".join([line.split()[0] for line in user_lines])
 
ps_output = os.popen('ps').read().strip() 
ps_lines = ps_output.split('\n')
ps_columns = ", ".join([line.split()[3] for line in ps_lines])

table = [
    ['Disk usage (MB):', disk_usage],
    ['Process count /w root:', process_count],
    ['Current cpu usage (%):', cpu_util],
    ['Current ram usage(%):', ram_util],
    ['Current users count:', current_users_count],
    ['Current user list:', user_columns],
    ['Current running processes:', ps_columns]
]

formatted_table = tabulate(table, headers=['Metric', 'Value'], stralign=("left",))

msg = MIMEText(formatted_table)
msg['Subject'] = 'System status report'
msg['From'] = 'petriixw@gmail.com'
msg['To'] = 'peterdano08@gmail.com'

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login('petriixw@gmail.com', 'priv-key')
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()
