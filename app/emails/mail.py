import smtplib
import re

from email.message import EmailMessage

from app.modules.songs.models import Song


class EmailParser:
    def __init__(self, template: str):
        self.template = template
    
    def get_subject(self, song_name: str) -> str:
        subject = 'Cool Demo - [SONG_NAME]'
        subject = subject.replace('[SONG_NAME]', song_name)
        return subject

    def get_message(self, email_type: str, song_link: str, contact_name: str, roster_name: str = None):
        template = self.template
        if email_type == 'Normal Email':
            message = 'We just finished this song demo and would love to get your feedback!'
            template = self.base_parsing(template=template, contact_name=contact_name, message=message, song_link=song_link)
            return template
        
        elif email_type == 'Management Email':
            message = 'Just finished this song demo that we think might be interesting for [ROSTER_NAME]! Would love to get your feedback on what you think or what you guys are looking for! Let us know!'
            message = message.replace('[ROSTER_NAME]', roster_name)
            template = self.base_parsing(template=template, contact_name=contact_name, message=message, song_link=song_link)
            return template
        
        elif email_type == 'General Email':
            message = 'We just finished this song demo and would love to get it into the right hands! If there is a better email for that, pls let us know!'
            template = self.base_parsing(template=template, contact_name=contact_name, message=message, song_link=song_link)
            return template

    def base_parsing(self, template, contact_name, message, song_link):
            template = template.replace('[CONTACT_NAME]', contact_name)
            template = template.replace('[MESSAGE]', message)
            template = template.replace('[SONG_LINK]', song_link)
            return template

    def get_recipients(self, song: Song):
        recipients = []
        for genre in song.genres:
            for contact in genre.contacts:
                if not contact.command:
                    continue
                if contact.command.name == 'Emailing':
                    if song not in contact.songs:
                        if self.validate_email(contact.email):
                            recipients.append(contact.email)
        return recipients

    def validate_email(self, email):
        pattern = r'[^@]+@[^@]+\.[^@]+'
        if not re.match(pattern, email):
            return False
        return True


class EmailSender:
    def __init__(
        self, 
        EMAIL_ADDRESS: str,
        EMAIL_PASSWORD: str, 
        recipient: str,
        subject: str,
        message: str
    ):
        self.EMAIL_ADDRESS = EMAIL_ADDRESS
        self.EMAIL_PASSWORD = EMAIL_PASSWORD
        self.recipient = recipient
        self.subject = subject
        self.message = message

    def send(self):
        msg = EmailMessage()
        msg['Subject'] = self.subject
        msg['From'] = self.EMAIL_ADDRESS
        msg.set_content(self.message)
        msg['To'] = self.recipient

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)
            smtp.send_message(msg)


