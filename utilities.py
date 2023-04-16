import os
import psutil
from pathlib import Path
from email_helpers import get_email_html_table

def get_column_from_cmd(cmd: str, column_index: int) -> None or str:
    output = os.popen(cmd).read().strip()
    if output == '':
        return None
    lines = output.split('\n')
    column = ", ".join([line.split()[column_index] for line in lines])
    return column

def get_monitoring_data() -> dict:
    disk_usage = os.popen("df --output=avail -BM / | awk 'NR==2'").read().strip()
    process_count = os.popen("ps -A | wc -l").read().strip()
    cpu_util = psutil.cpu_percent()
    ram_util = psutil.virtual_memory().percent
    current_users_count = os.popen("who | wc -l").read().strip()
    users = get_column_from_cmd("who", 0) or 'no users'
    processes = get_column_from_cmd("ps", 3) or 'no processes'

    return {
        "disk_usage": disk_usage,
        "process_count": process_count,
        "cpu_util": cpu_util,
        "ram_util": ram_util,
        "current_users_count": current_users_count,
        "users": users,
        "processes": processes
    }

def get_monitoring_data2() -> dict:
    uptime = os.popen("uptime | awk '{print $3}'").read().strip()
    load_average5 = os.popen("uptime | awk '{print $8}'").read().strip()
    load_average15 = os.popen("uptime | awk '{print $9}'").read().strip()
    current_date = os.popen("date").read().strip()
    return {
        "uptime": uptime,
        "load_average5": load_average5,
        "load_average15": load_average15,
        "current_date": current_date
    }

def load_html(data: dict, data2: dict) -> str:
    file_path = Path(__file__).with_name('index.html')
    html = open(file_path, "r").read()
    html = html.replace("{$email_table}", get_email_html_table(data))
    html = html.replace("{$uptime}", data2["uptime"])
    html = html.replace("{$load_average5}", data2["load_average5"])
    html = html.replace("{$load_average15}", data2["load_average15"])
    html = html.replace("{$current_date}", data2["current_date"])
    return html
