import smtplib
import re

from email.message import EmailMessage
from typing import List, Optional
from app.modules.contacts.models import Contact

from app.modules.songs.models import Song


class EmailParser:
    def __init__(self, template: str):
        self.template = template

    def get_subject(self, song_name: str) -> str:
        subject = "Friendly Neighborhood Music"
        subject = subject.replace("[SONG_NAME]", song_name)
        return subject

    def get_message(
        self,
        email_type: str,
        song_link: str,
        contact_name: str,
        roster_name: Optional[str] = None,
    ):
        template = self.template
        if email_type == "Normal Email":
            message = "We made this demo and we would like to pitch it to you. Would love to get your feedback on what you think or what you guys are looking for! Let us know!"
            template = self.base_parsing(
                template=template,
                contact_name=contact_name,
                message=message,
                song_link=song_link,
            )
            return template

        elif email_type == "Management Email":
            message = "We made this demo that we think might be interesting for one of your artists! Would love to get your feedback on what you think or what you guys are looking for! Let us know!"
            template = self.base_parsing(
                template=template,
                contact_name=contact_name,
                message=message,
                song_link=song_link,
            )
            return template

        elif email_type == "General Email":
            message = "We made this demo and we would like to pitch it and get it into the right hands! If there is a better email for that, pls let us know!"
            template = self.base_parsing(
                template=template,
                contact_name=contact_name,
                message=message,
                song_link=song_link,
            )
            return template

        elif email_type == "RAMPAK Email":
            message = "We are a producer duo called RAMPAK, and we just finished up this demo. We would love to get your feedback!"
            template = self.base_parsing(
                template=template,
                contact_name=contact_name,
                message=message,
                song_link=song_link,
                author="RAMPAK",
            )
            return template

    def base_parsing(self, template, contact_name, message, song_link, author="PJCrew"):
        template = template.replace("[CONTACT_NAME]", contact_name)
        template = template.replace("[MESSAGE]", message)
        template = template.replace("[SONG_LINK]", song_link)
        template = template.replace("[AUTHOR]", author)
        return template

    def get_recipients(
        self, song: Song, all_genre_contacts: List[Contact]
    ) -> List[str]:
        recipients = []
        for genre in song.genres:
            recipients += self._get_valid_emails(song, genre.contacts)
        # Include Contacts with All Genres
        recipients += self._get_valid_emails(song, all_genre_contacts)
        return sorted(list(set(recipients)))

    def _get_valid_emails(self, song: Song, contacts: List[Contact]) -> List[str]:
        recipients = []
        for contact in contacts:
            if not self._validate_contact(contact, song):
                continue
            for email_address in contact.emails:
                if self.validate_email(email_address):
                    recipients.append(email_address)
            return recipients

    def _validate_contact(self, contact, song):
        if contact.command.name != "Emailing":
            return False
        if song in contact.songs:
            return False
        return True

    def validate_email(self, email):
        pattern = r"[^@]+@[^@]+\.[^@]+"
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
        message: str,
    ):
        self.EMAIL_ADDRESS = EMAIL_ADDRESS
        self.EMAIL_PASSWORD = EMAIL_PASSWORD
        self.recipient = recipient
        self.subject = subject
        self.message = message

    def send(self):
        msg = EmailMessage()
        msg["Subject"] = self.subject
        msg["From"] = self.EMAIL_ADDRESS
        msg.set_content(self.message)
        msg["To"] = self.recipient

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)
            smtp.send_message(msg)
