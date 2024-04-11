import logging
import smtplib
from email.message import EmailMessage

from NeonPong import settings


class MailClient:
    def __init__(self):
        self.server = smtplib.SMTP(
            settings.SMTP_SERVER, settings.SMTP_PORT
        )
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)

    def send_mail(self, mail, subject, reply_to, message, subtype="plain"):
        msg = EmailMessage()
        msg.set_content(message, subtype=subtype)
        msg["Subject"] = subject
        msg["From"] = settings.MAIL_USERNAME
        msg["To"] = mail
        msg["Reply-To"] = reply_to
        try:
            logging.info(f'MSG: {self.server.send_message(msg)}')
        except Exception as e:
            logging.error(e)

    def quit(self):
        self.server.quit()

    def __del__(self):
        try:
            self.quit()
        except Exception:
            pass
