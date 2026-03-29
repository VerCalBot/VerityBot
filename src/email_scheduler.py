import datetime
import logging
from crontab import CronTab
from ConfigReader import config

cron = CronTab(user=True)

def _verify_time_format(date_str: str) -> list[str]:
    try:
        datetime.datetime.strptime(date_str, '%H:%M')
    except ValueError:
        logging.error("Invalid EMAIL_SEND_TIME, must be 24-hour format")
        exit(1)
    return date_str.split(':')

def create_cron_job():
    mail_time = config ['Email'] ['EMAIL_SEND_TIME']
    hours, mins = _verify_time_format(mail_time)

    script_path = '/Users/jalen/git/VerityBot/src/send_email.py'
    python_executable = '/usr/bin/python3'
    command = f'{python_executable} {script_path}'

    job = cron.new(command=command, comment='Kibana Dashboard Email')

    # schedule the job to run every day at EMAIL_SEND_TIME
    job.minute.on(int(mins))
    job.hour.on(int(hours))
    job.day.every(1)  # Run every day
    # the other fields (month, day of week) default to '*' which means every

    # write the job to the crontab
    cron.write()
    print(f"Scheduled job: {command} to run daily at {mail_time}")

create_cron_job()
