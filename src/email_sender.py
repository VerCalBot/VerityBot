import logging
import os
import smtplib
import socket
import subprocess
import Utils

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ConfigReader import config

recipient_email = config ['Email'] ['EMAIL_TO']
sender_email = config ['Email'] ['EMAIL_FROM']
email_subject = config ['Email'] ['EMAIL_SUBJECT']

domain_to_server_mapping: dict = {
        "gmail.com": "gmail.com", 
        "outlook.com": "office365.com",
        "louisville.edu": "office365.com",
        "shslou.org": "office365.com"
}

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = email_subject

def domain_to_server(email: str) -> str | None:
    if '@' in email:
        domain = email[email.index('@') + 1:]
        smtp_server = domain_to_server_mapping.get(domain, None)
        return smtp_server
    return None

def send_email():
    smtp_server = domain_to_server(sender_email)
    if smtp_server:
        try:
            with smtplib.SMTP(f"smtp.{smtp_server}", 587) as s:
                s.set_debuglevel(1)
                s.starttls()
                s.login(sender_email, str(email_password))
                s.sendmail(sender_email, recipient_email, message.as_string())
                s.quit()
        except Exception as e:
            logging.error(f"Unable to send email: error code {e.args.index}")
            exit(1)
    else:
        logging.error("Unable to send email. Make sure the sender email is correct!")

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

script_path = Utils.get_project_root() / "scripts" / "get_ip.sh"
subprocess.run([script_path], check=True)

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
        <a href="https://{IP}:5601/app/dashboards">Kibana Dashboards</a>
    </body>
</html>
"""

message.attach(MIMEText(html, "html"))

email_password = os.getenv("EMAIL_PASSWORD")

send_email()

