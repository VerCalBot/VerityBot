import os
import smtplib
import schedule
import time
import datetime
import logging
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

html = f"""
<html>
  <body>
    <p>Click the link below to access the Kibana dashboard:</p>
    <a href="https://192.168.1.51">Kibana Dashboard</a>
  </body>
</html>
"""
message.attach(MIMEText(html, "html"))

load_dotenv()
email_password = os.getenv("EMAIL_PASSWORD")
mail_time = config ['Email'] ['EMAIL_SEND_TIME']

def _verify_time_format(date_str: str):
    try:
        datetime.datetime.strptime(date_str, '%H:%M')
    except ValueError:
        logging.error("Invalid EMAIL_SEND_TIME format (must be 24-hour format)")
        exit(1)

def send_email():
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(sender_email, str(email_password))
            s.sendmail(sender_email, recipient_email, message.as_string())
            s.quit()
    except Exception as e:
        logging.error("Unable to send email")
        exit(1)

def schedule_email():
    _verify_time_format(mail_time)
    schedule.every().friday.at(mail_time).do(send_email)
    while True:
        schedule.run_pending()
        time.sleep(1)

send_email()
