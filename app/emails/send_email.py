import os

from .sender import EmailSender
from app.db.database import get_db
from app.modules.contacts.models import Contact
from app.modules.songs.models import Song


if __name__ == "__main__":
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    recipients = ['guilhermebilton@hotmail.com']
    subject = "Friendly Neighborhood Music"

    with open(r'app/emails/templates/sunday_cold.html', 'r') as f:
        text = f.read()
    
    session = next(get_db())
    contacts = session.query(Contact).all()
    songs = session.query(Song).all()

    for contact, song in zip(contacts, songs):
        message = text.replace('[CONTACT_NAME]', contact.name)
        message = message.replace('[SONG_LINK]', f'<a href="{song.link}">{song.name}</a>')


        mail = EmailSender(EMAIL_ADDRESS=EMAIL_ADDRESS,
        EMAIL_PASSWORD=EMAIL_PASSWORD,
        contacts=recipients,
        subject=subject,
        message=message)

        mail.send()
