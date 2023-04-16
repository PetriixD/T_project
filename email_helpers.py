import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_email_html_table(data: dict) -> str:
    def get_table_row(key: str) -> str:
        return f"""
        <tr>
            <td>{data_labels[key]}:</td>
            <td>{data[key]}</td>
        </tr>
        """
    data_labels = {
        "disk_usage": "Disk usage (MB)",
        "process_count": "Process count /w root",
        "cpu_util": "Current cpu usage (%)",
        "ram_util": "Current ram usage(%)",
        "current_users_count": "Current users count",
        "users": "Current user list",
        "processes": "Current running processes"
    }
    html_table = f"""
        <table>
        <tr>
            <th align="left">Metric</th>
            <th align="left">Value</th>
        </tr>
        {''.join([get_table_row(key) for key in data.keys()])}
    </table>
    """
    return html_table

def get_email_message(subject: str, email_from: str, email_to: str, html: str) -> MIMEMultipart:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to
    part = MIMEText(html, 'html')
    msg.attach(part)
    return msg

def send_email(login: str, password: str, msg: MIMEMultipart) -> None:
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(login, password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
