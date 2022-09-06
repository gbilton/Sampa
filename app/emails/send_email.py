import os
import time
from email.mime.text import MIMEText

from tqdm import tqdm

from app.db.database import get_db
from app.emails.email_logger import logging
from app.models import EmailAddress, EmailType, Genre, Song

from .mail import EmailParser, EmailSender

if __name__ == "__main__":
    session = next(get_db())

    EMAIL_ADDRESS = os.environ.get("RAMPAK_EMAIL")
    EMAIL_PASSWORD = os.environ.get("RAMPAK_AUTH")

    if not EMAIL_ADDRESS:
        raise Exception("No Email Address")
    if not EMAIL_PASSWORD:
        raise Exception("No Email Password")

    with open(r"app/emails/templates/RAMPAK_template.txt", "r") as f:
        template = f.read()

    parser = EmailParser(template)

    song_name = "Chase It"
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
            # email_type=email_type.name, # HACK: When song genre == "EDM", change to "RAMPAK Email"
            email_type="RAMPAK Email",
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
            # recipient="ralie139@gmail.com",
            subject=subject,
            message=MIMEText(message, "html"),
        )
        # To send an email, change song_name, recipient and uncomment code below

        try:
            pass
            mail.send()
            logging.warning(
                f"Mail Sent. Sent from: {EMAIL_ADDRESS}. Contact: {contact.name}. Recipient: {recipient}. Song: {song.name}. Email Type: {email_type.name}"
            )
        except Exception:
            try:
                print("SMTP Error, attempting again in 5 minutes...")
                time.sleep(5 * 60)
                mail.send()
                print("Resumed successfully :)")
            except Exception:
                raise Exception("Failed to send email :(")
        email.songs.append(song)
        session.add(email)
        session.commit()
