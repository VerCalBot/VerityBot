import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.office365.com',587)

s.starttls()

s.login("sender_email","sender_pass")

content = "link_to_Kibana"

s.sendmail("sender_email","receiver_email",content)

s.quit()
