import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.client import HTTPException
import smtplib
import ssl
from uuid import uuid4

def generate_id():
    return base64.urlsafe_b64encode(uuid4().bytes).decode('utf-8').strip('=')

def server_send_mail(smtp_config: dict, server,
                     subject: str, to: str, msg: str):
    sender_email = smtp_config['MAIL_SENDER']
    password_mail = smtp_config['MAIL_PASSWORD']
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = to
    message.attach(MIMEText(msg, 'html'))
    server.login(sender_email, password_mail)
    server.sendmail(sender_email, to, message.as_string())


def send_mail(smtp_config: dict, subject: str, to: str, msg: str):
    try:
        context = ssl.create_default_context()
        port_mail = smtp_config['MAIL_PORT']
        server_mail = smtp_config['MAIL_SERVER']
        if smtp_config['MAIL_SSL']:
            # Create a secure SSL context
            with smtplib.SMTP_SSL(
                    server_mail, port_mail, context=context) as server:
                server_send_mail(smtp_config, server, subject, to, msg)
        else:
            # With security TLS
            with smtplib.SMTP(server_mail, port_mail) as server:
                if smtp_config['MAIL_TLS']:
                    server.starttls(context=context)
                server_send_mail(smtp_config, server, subject, to, msg)
    except OSError:
        raise HTTPException('Invalid SMTP configuration')