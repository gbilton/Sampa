import os

from tqdm import tqdm
from app.emails.email_logger import logging
from app.db.database import get_db
from app.models import *

from .mail import EmailSender, EmailParser


if __name__ == "__main__":
    session = next(get_db())

    EMAIL_ADDRESS = os.environ.get("PJCREW_EMAIL")
    EMAIL_PASSWORD = os.environ.get("PJCREW_AUTH")

    if not EMAIL_ADDRESS:
        raise Exception("No Email Address")
    if not EMAIL_PASSWORD:
        raise Exception("No Email Password")

    with open(r"app/emails/templates/Base Email.txt", "r") as f:
        template = f.read()

    parser = EmailParser(template)

    song_name = "Sleep Alone"
    song = session.query(Song).filter_by(name=song_name).first()
    all_genre = session.query(Genre).filter_by(name="All Genres").first()

    if not song:
        raise Exception("Song Not Found!")

    recipients = parser.get_recipients(song, all_genre.contacts)
    subject = parser.get_subject(song.name)

    for recipient in tqdm(recipients):
        email = session.query(EmailAddress).filter_by(address=recipient).first()
        contact = email.contact
        email_type = session.query(EmailType).filter_by(id=email.email_type_id).first()

        if not email_type:
            continue

        roster_name = None

        message = parser.get_message(
            email_type=email_type.name,  # HACK: When song genre == "EDM", change to "RAMPAK Email"
            song_link=song.link,
            contact_name=contact.name,
            roster_name=roster_name,
        )

        if not message:
            raise Exception("No Message to send.")

        mail = EmailSender(
            EMAIL_ADDRESS=EMAIL_ADDRESS,
            EMAIL_PASSWORD=EMAIL_PASSWORD,
            recipient=recipient,
            subject=subject,
            message=message,
        )

        # To send an email, change song_name, recipient and uncomment code below

        try:
            pass
            mail.send()
            logging.warning(
                f"Mail Sent. Contact: {contact.name}. Recipient: {recipient}. Song: {song.name}. Email Type: {email_type.name}"
            )
        except:
            raise Exception("Failed to send email :(")

        email.songs.append(song)
        session.add(email)
        session.commit()
