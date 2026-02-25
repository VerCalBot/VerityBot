import os
import smtplib
import configparser
import schedule
import time
import re
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

def send_email():
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.set_debuglevel(1)
    s.starttls()
    s.login(sender_email, email_password)
    s.sendmail(sender_email,recipient_email,message.as_string())
    s.quit()

mail_time = config ['Email'] ['EMAIL_SEND_TIME']
h, m, am_pm = re.findall(r'\d+|\w+', mail_time)
hour = int(h)
mins = int(m)
if am_pm.lower() == 'pm' and hour != 12:
    hour += 12
elif am_pm.lower() == 'am' and hour == 12:
    hour = 0

mail_time = f'{hour:02d}:{mins:02d}'
print(mail_time)


schedule.every().day.at("07:24").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(60)
