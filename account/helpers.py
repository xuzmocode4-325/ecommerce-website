import os
from django.core.mail import mail_admins, get_connection, send_mail, BadHeaderError

EMAIL_HOST = os.getenv('SMTP')
EMAIL_HOST_USER = os.getenv('USER')
EMAIL_HOST_PASSWORD = os.getenv('PASSWORD')

# Constants for email ports
SSL_PORT = 465
TLS_PORT = 587

# Fetch environment variables
import logging

# Set up logging
logger = logging.getLogger(__name__)

def create_email_connection(use_ssl: bool):
    return get_connection(
        host=EMAIL_HOST,
        port=SSL_PORT if use_ssl else TLS_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        use_ssl=use_ssl,
        use_tls=not use_ssl
    )

def send_email_with_fallback(subject, message, recipients):
    if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
        logger.error('Email host user or password not set in environment variables.')
        return False

    def attempt_send_email(use_ssl):
        try:
            connection = create_email_connection(use_ssl=use_ssl)
            send_mail(
                subject=subject, message=message, from_email=EMAIL_HOST_USER,
                recipient_list=recipients, connection=connection
            )
            logger.info(f'Email sent successfully using {"SSL" if use_ssl else "TLS"}.')
            return True
        except BadHeaderError:
            logger.error('BadHeaderError encountered while sending email.')
        except Exception as e:
            logger.error(f'An error occurred while sending email via {"SSL" if use_ssl else "TLS"}: {e}')
        return False

    # Attempt to send email using SSL, fallback to TLS if it fails
    return attempt_send_email(use_ssl=True) or attempt_send_email(use_ssl=False)