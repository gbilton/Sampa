import smtplib

from email.message import EmailMessage
from typing import List

class EmailSender:
    def __init__(
        self, 
        EMAIL_ADDRESS: str,
        EMAIL_PASSWORD: str, 
        contacts: List[str],
        subject: str,
        message: str
    ):
        self.EMAIL_ADDRESS = EMAIL_ADDRESS
        self.EMAIL_PASSWORD = EMAIL_PASSWORD
        self.contacts = contacts
        self.subject = subject
        self.message = message

    def send(self):
        msg = EmailMessage()
        msg['Subject'] = self.subject
        msg['From'] = self.EMAIL_ADDRESS
        msg.set_content(self.message,'html')

        for recipient in self.contacts:
            msg['To'] = recipient


            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)
                smtp.send_message(msg)
