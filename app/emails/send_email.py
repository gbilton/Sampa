import os

from app.emails.email_logger import logging
from app.db.database import get_db
from app.models import *

from .mail import EmailSender, EmailParser


if __name__ == "__main__":
    session = next(get_db())

    EMAIL_ADDRESS = os.environ.get('PJCREW_EMAIL')
    EMAIL_PASSWORD = os.environ.get('PJCREW_AUTH')

    if not EMAIL_ADDRESS:
        raise Exception("No Email Address")
    if not EMAIL_PASSWORD:
        raise Exception("No Email Password")

    with open(r'app/emails/templates/Base Email.txt', 'r') as f:
        template = f.read()

    parser = EmailParser(template)

    song_name = 'Psycho'
    song = session.query(Song).filter_by(name=song_name).first()
    
    if not song:
        raise Exception('Song Not Found!')
    
    recipients = parser.get_recipients(song)
    subject = parser.get_subject(song.name)

    for recipient in recipients:
        contact = session.query(Contact).filter_by(email=recipient).first()
        email_type = session.query(EmailType).filter_by(id=contact.email_type_id).first()
        
        if not email_type:
            continue
        
        roster_name = None
        if email_type.name == "Management Email":
            if not contact.rosters:
                email_type.name = 'Normal Email'
            else:
                roster_name = contact.rosters[0].name


        message = parser.get_message(
            email_type=email_type.name,
            song_link=song.link,
            contact_name=contact.name,
            roster_name=roster_name
        )


        if not message:
            raise Exception("No Message to send.")


        mail = EmailSender(EMAIL_ADDRESS=EMAIL_ADDRESS,
        EMAIL_PASSWORD=EMAIL_PASSWORD,
        recipient='guilhermebilton@gmail.com',
        subject=subject,
        message=message)
        
        try:
            # mail.send()
            logging.warning(f"Mail sent to {contact.name}: {recipient}")
        except:
            raise Exception('Failed to send email :(')

        # contact.songs.append(song)
        # session.add(contact)
        # session.commit()