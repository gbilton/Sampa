import os
import re
import smtplib
import time
from email.message import EmailMessage
from enum import Enum
from typing import List, Tuple

from sqlalchemy import insert

from app.db.database import get_db
from app.modules.contacts.models import Contact
from app.modules.emails.models import EmailAddress, sent_table
from app.modules.songs.models import Song
from app.modules.songs.schemas import SongGenreEnum


class EmailTemplateEnum(str, Enum):
    rampak_template = "RAMPAK_Template"
    pjcrew_template = "PJCREW_Template"


class EmailParser:
    def __init__(self, template: EmailTemplateEnum):
        self.template = template

    def get_subject(self) -> str:
        if self.template == EmailTemplateEnum.rampak_template:
            subject = "Greetings earthlings let us know what you think!"
        elif self.template == EmailTemplateEnum.pjcrew_template:
            subject = "Hope you're having a jolly good week!"
        else:
            raise Exception(f"Invalid template: '{self.template}'")
        return subject

    def get_message(
        self,
        song_link: str,
        contact_name: str,
        song_name: str,
    ):
        if self.template == EmailTemplateEnum.rampak_template:
            with open("app/emails/templates/RAMPAK Template.txt", "r") as f:
                template = f.read()
            message = """<html>
                <body>

                <p>We’re a fresh out of the oven producer duo called RAMPAK and we just released our first ever song called <a href="https://orcd.co/liveanotherday">Live Another Day</a>.</p>
                <p>So far people seem to really like it, but we want to keep dropping new and exciting music. That’s why we would love to hear what you guys think about our newest demo down below.</p>
                <p>https://soundcloud.com/rampak/chase-it</p>
                <p>Please give us your honest thoughts and hit us up if you’re interested. Can’t wait to hear back.<p/>
                <p><a href="http://instagram.com/rampakmusic">RAMPAK Instagram</a></p>
                </body>
                </html>
            """

            final_message = self.base_parsing(
                template=template,
                contact_name=contact_name,
                message=message,
                song_link=song_link,
                song_name=song_name,
                author="Pie and Raff aka RAMPAK",
            )

        elif self.template == EmailTemplateEnum.pjcrew_template:
            with open("app/emails/templates/PJCREW Template.txt", "r") as f:
                template = f.read()
            message = "We are Pie and Raff, a songwriting and production duo. We made this demo that we think might be interesting for you guys! Would love to get your feedback on what you think or what you guys are looking for. Let us know!"
            final_message = self.base_parsing(
                template=template,
                contact_name=contact_name,
                message=message,
                song_link=song_link,
                song_name=song_name,
                author="Pie and Raff aka PJCrew",
            )
        else:
            raise Exception(f"Invalid template: '{self.template}'")
        return final_message

    def base_parsing(self, template, contact_name, message, song_link, song_name, author="PJCrew"):
        template = template.replace("[CONTACT_NAME]", contact_name)
        template = template.replace("[MESSAGE]", message)
        template = template.replace("[SONG_LINK]", song_link)
        template = template.replace("[AUTHOR]", author)
        template = template.replace("[SONG_NAME]", song_name)
        return template

    def get_recipients(self, song: Song, all_genre_contacts: List[Contact]) -> List[str]:
        recipients = []
        for genre in song.genres:
            recipients += self._get_valid_emails(song, genre.contacts)
        # Include Contacts with All Genres
        recipients += self._get_valid_emails(song, all_genre_contacts)
        return sorted(list(set(recipients)))

    def _get_valid_emails(self, song: Song, contacts: List[Contact]) -> List[str]:
        recipients = []
        for contact in contacts:
            for email in contact.emails:
                if not self._validate_email_command(email):
                    continue
                if not self._validate_email_string(email.address):
                    continue
                if self._check_if_already_sent(email, song):
                    continue
                recipients.append(email.address)
        return recipients

    def _check_if_already_sent(self, email: EmailAddress, song: Song) -> bool:
        if song in email.songs:
            return True
        return False

    def _validate_email_command(self, email: EmailAddress) -> bool:
        if email.command.name != "Emailing":
            return False
        return True

    def _validate_email_string(self, email: str) -> bool:
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


class EmailService:
    def get_email_object(self, session, address: str) -> EmailAddress:
        email_address = session.query(EmailAddress).filter_by(address=address).first()
        if not email_address:
            raise Exception("Recipient Email not found.")
        return email_address

    def send_email(self, mail: EmailSender):
        try:
            mail.send()
        except Exception:
            try:
                self.try_again(mail=mail, minutes=10)
            except Exception:
                raise Exception("Failed to send email :(")

    def try_again(self, mail: EmailSender, minutes: int):
        print(f"SMTP Error, attempting again in {minutes} minutes...")
        time.sleep(minutes * 60)
        mail.send()
        print("Resumed successfully :)")

    def compose_email(
        self,
        recipient: str,
        subject: str,
        email_template: EmailTemplateEnum,
        song: Song,
        email_address: str,
        email_password: str,
        session,
    ):
        email_object = self.get_email_object(session, address=recipient)
        contact = email_object.contact

        parser = EmailParser(email_template)
        message = parser.get_message(
            song_link=song.link,
            contact_name=contact.name,
            song_name=song.name,
        )

        if not message:
            raise Exception("No Message to send.")

        mail_sender = EmailSender(
            EMAIL_ADDRESS=email_address,
            EMAIL_PASSWORD=email_password,
            recipient=recipient,
            subject=subject,
            message=message,
        )
        return mail_sender, email_object

    def register_to_db(self, email_object: EmailAddress, song: Song):
        with next(get_db()) as conn:
            try:
                conn.execute(
                    insert(sent_table),
                    {"Song ID": song.id, "Email Address ID": email_object.id},
                )
                conn.commit()
            except Exception:
                raise Exception("Could not insert sent song to database.")

    def get_email_headline(self, song_genres: list[SongGenreEnum]) -> Tuple[str, str, str]:
        if SongGenreEnum.edm in song_genres:
            if len(song_genres) != 1:
                raise Exception("EDM must be unique song genre.")
            email = "RAMPAK_EMAIL"
            password = "RAMPAK_AUTH"
            template = EmailTemplateEnum.rampak_template
        else:
            email = "PJCREW_EMAIL"
            password = "PJCREW_AUTH"
            template = EmailTemplateEnum.pjcrew_template
        return email, password, template

    def set_email_headline(self, email: str, password: str):
        EMAIL_ADDRESS = os.environ.get(email)
        EMAIL_PASSWORD = os.environ.get(password)
        if not EMAIL_ADDRESS:
            raise Exception("No Email Address")
        if not EMAIL_PASSWORD:
            raise Exception("No Email Password")
        return EMAIL_ADDRESS, EMAIL_PASSWORD
