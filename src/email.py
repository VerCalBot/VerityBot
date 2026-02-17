import os
import smtplib
import configparser
from dotenv import load_dotenv

config = configparser.ConfigParser()
config.read("../config.ini")

# Assign variables from ini
recipient_email = config ['Email'] ['EMAIL_TO']
sender_email = config ['Email'] ['EMAIL_FROM']
message = config ['Email'] ['EMAIL_MESSAGE']

load_dotenv()
# Retrieve password from env
email_password = os.getenv("EMAIL_PASSWORD")

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com',587)

s.set_debuglevel(1)

s.starttls()

s.login(sender_email, email_password)

s.sendmail(sender_email,recipient_email,message)

s.quit()
