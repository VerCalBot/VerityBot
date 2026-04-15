import logging
import os
import smtplib
import socket

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ConfigReader import config

recipient_email = config ['Email'] ['EMAIL_TO']
sender_email = config ['Email'] ['EMAIL_FROM']
email_subject = config ['Email'] ['EMAIL_SUBJECT']

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = email_subject

def send_email():
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(sender_email, str(email_password))
            s.sendmail(sender_email, recipient_email, message.as_string())
            s.quit()
    except Exception as e:
        logging.error(f"Unable to send email: error code {e.args.index}")
        exit(1)

# for sending the link to Kibana through email
# IP address is likely to change due to proxies or DHCP lease termination
# this function attempts to connect to a host, resolves to localhost if no connection is made
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

load_dotenv()
IP = os.getenv("WINDOWS_IP") or get_ip()

# read prefix only from config (no env fallback)
body_prefix = config['Email'].get(
        'EMAIL_BODY_PREFIX', 'Click the link below to access the Kibana dashboard:'
)

html = f"""
<html>
    <body>
        <p>{body_prefix}</p>
        <a href="https://{IP}:5601/app/dashboards">Kibana Dashboard</a>
    </body>
</html>
"""

message.attach(MIMEText(html, "html"))

email_password = os.getenv("EMAIL_PASSWORD")

send_email()
