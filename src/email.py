import os
import smtplib
import configparser
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

config = configparser.ConfigParser()
config.read("../config.ini")

recipient_email = config ['Email'] ['EMAIL_TO']
sender_email = config ['Email'] ['EMAIL_FROM']
email_subject = config ['Email'] ['EMAIL_SUBJECT']
email_message = config ['Email'] ['EMAIL_MESSAGE']

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = email_subject
body = email_message
message.attach(MIMEText(body, "plain"))

load_dotenv()
email_password = os.getenv("EMAIL_PASSWORD")

s = smtplib.SMTP('smtp.gmail.com',587)

s.set_debuglevel(1)

s.starttls()

s.login(sender_email, email_password)

s.sendmail(sender_email,recipient_email,message.as_string())

s.quit()

