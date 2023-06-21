import argparse
import logging
from typing import Optional

from tqdm import tqdm

from app.db.database import get_db
from app.modules.genres.services import GenreService
from app.modules.songs.schemas import SongGenreEnum
from app.modules.songs.services import SongService

from .mail import EmailParser, EmailService

parser = argparse.ArgumentParser(description="Send emails.")
parser.add_argument(
    "songs",
    type=str,
    help="Song to test",
)
parser.add_argument(
    "--subject",
    type=str,
    help="Email's subject",
)


args = parser.parse_args()
song_name = args.songs
subject = args.subject


def main(song_name: str, subject: Optional[str], recipients: Optional[list[str]]):
    session = next(get_db())
    song = SongService.get_song(session, song_name)
    song_genres = song.genres
    if not song_genres:
        raise Exception(f"Song {song.name} has no genre.")
    song_genres = [genre.name for genre in song_genres]

    email_service = EmailService()
    email_to_use, password_to_use, template = email_service.get_email_headline(
        song_genres
    )
    EMAIL_ADDRESS, EMAIL_PASSWORD = email_service.set_email_headline(
        email_to_use, password_to_use
    )

    all_genre = GenreService.get_genre(session, SongGenreEnum.all_genre)
    email_parser = EmailParser(template)

    if not recipients:
        recipients = email_parser.get_recipients(song, all_genre.contacts)

    if not subject:
        subject = email_parser.get_subject()

    for recipient in tqdm(recipients):
        mail_sender, email_object = email_service.compose_email(
            recipient=recipient,
            subject=subject,
            email_template=template,
            song=song,
            email_address=EMAIL_ADDRESS,
            email_password=EMAIL_PASSWORD,
            session=session,
        )
        email_service.send_email(mail_sender)
        logging.info(
            f"Mail Sent. Sent from: {mail_sender.EMAIL_ADDRESS}. Recipient: {mail_sender.recipient}. Song: {song.name}. Email Template: {template}"
        )
        email_service.register_to_db(email_object=email_object, song=song)


if __name__ == "__main__":
    main(song_name, subject, recipients=None)
