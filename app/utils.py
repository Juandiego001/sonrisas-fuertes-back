import base64
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.client import HTTPException
import smtplib
import ssl
from uuid import uuid4
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt,\
    set_access_cookies, unset_jwt_cookies
from app import app, jwt
from app.schemas.account import Profile 

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


def success_message():
    return {'message': 'Guardado extiosamente'}


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=15))
        if target_timestamp > exp_timestamp:
            data_profile = Profile().dump(get_jwt())
            access_token = create_access_token(
                identity=str(data_profile['_id']),
                additional_claims=data_profile)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@jwt.expired_token_loader
def check_if_token_is_expired(jwt_header, jwt_payload: dict):
    response = jsonify({'message': 'Sesión expirada.\
                        Por favor, volver a iniciar sesión'})
    unset_jwt_cookies(response)
    return response, 401