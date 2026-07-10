import base64
import logging
import os
import smtplib
import socket
import subprocess
import Utils

import msal

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
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

# Microsoft 365 has disabled Basic Authentication (username/password) for SMTP
# AUTH. Instead we authenticate with an OAuth2 access token using the SMTP
# XOAUTH2 mechanism. The token is obtained app-only (client credentials) from
# Microsoft Entra ID using an app registration authenticated with a certificate
# -- see the "Microsoft 365 email setup" section of the README for how to create
# the app, upload the certificate, and grant it the SMTP.SendAsApp permission
# scoped to the sender mailbox.

# Build the MSAL certificate credential from a PEM file that contains both the
# private key and the certificate. MSAL needs the private key plus the cert's
# SHA-1 thumbprint, which we compute here so the operator never has to copy it.
def load_client_credential() -> dict:
    with open(cert_path, "rb") as f:
        pem_data = f.read()
    cert = x509.load_pem_x509_certificate(pem_data)
    return {
        "private_key": pem_data.decode(),
        "thumbprint": cert.fingerprint(hashes.SHA1()).hex(),
        "public_certificate": cert.public_bytes(serialization.Encoding.PEM).decode(),
    }

def get_access_token() -> str:
    if not (tenant_id and client_id and cert_path):
        raise RuntimeError(
            "Missing Microsoft 365 credentials. AZURE_TENANT_ID, AZURE_CLIENT_ID "
            "and AZURE_CERT_PATH must all be set in the .env file "
            "(run the setup dialogue box to configure them)."
        )
    if not os.path.isfile(cert_path):
        raise RuntimeError(f"Certificate file not found: {cert_path}")

    app = msal.ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=load_client_credential(),
    )
    # ".default" requests the application permissions already consented to the
    # app registration (i.e. SMTP.SendAsApp on Office 365 Exchange Online).
    result = app.acquire_token_for_client(
        scopes=["https://outlook.office365.com/.default"]
    )
    if "access_token" not in result:
        raise RuntimeError(
            "Unable to acquire Microsoft 365 access token: "
            f"{result.get('error_description', result)}"
        )
    return result["access_token"]

def send_email():
    smtp_server = domain_to_server(sender_email)
    if not smtp_server:
        logging.error("Unable to send email. Make sure the sender email is correct!")
        return

    try:
        access_token = get_access_token()
        # XOAUTH2 SASL initial-response string; smtplib base64-encodes it for us.
        auth_string = f"user={sender_email}\1auth=Bearer {access_token}\1\1"

        with smtplib.SMTP(f"smtp.{smtp_server}", 587) as s:
            s.set_debuglevel(1)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.auth("XOAUTH2", lambda challenge=None: auth_string)
            s.sendmail(sender_email, recipient_email, message.as_string())
    except Exception as e:
        logging.error(f"Unable to send email: {e}")
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

script_path = Utils.get_project_root() / "scripts" / "get_ip.sh"
subprocess.run([script_path], check=True)

# Load .env from the project root explicitly so this works when cron runs the
# script from an arbitrary working directory.
load_dotenv(Utils.get_project_root() / ".env")
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

# Microsoft 365 app-only (certificate credentials) OAuth2 credentials.
tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
cert_path = os.getenv("AZURE_CERT_PATH")

send_email()

