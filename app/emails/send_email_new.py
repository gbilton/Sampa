import argparse
import logging

from tqdm import tqdm

from app.modules.genres.services import GenreService
from app.modules.songs.schemas import SongGenreEnum
from app.modules.songs.services import SongService

from .mail import EmailParser, EmailService

parser = argparse.ArgumentParser(description="Send test email.")
parser.add_argument(
    "songs",
    type=str,
    help="Song to send",
)

args = parser.parse_args()
song_name = args.songs


def main(song_name: str):
    song = SongService.get_song(song_name)
    song_genres = song.genres
    if not song_genres:
        raise Exception(f"Song {song.name} has no genre.")

    email_service = EmailService()
    email_to_use, password_to_use, template = email_service.get_email_headline(song_genres)
    EMAIL_ADDRESS, EMAIL_PASSWORD = email_service.set_email_headline(email_to_use, password_to_use)

    all_genre = GenreService.get_genre(SongGenreEnum.all_genre)
    email_parser = EmailParser(template)
    recipients = email_parser.get_recipients(song, all_genre.contacts)
    subject = email_parser.get_subject(song.name)

    for recipient in tqdm(recipients):
        mail_sender, email_object = email_service.compose_email(
            recipient=recipient,
            subject=subject,
            email_template=template,
            song=song,
            email_address=email_to_use,
            email_password=password_to_use,
        )
        email_service.send_email(mail_sender)
        logging.info(
            f"Mail Sent. Sent from: {mail_sender.EMAIL_ADDRESS}. Recipient: {mail_sender.recipient}. Song: {song.name}. Email Template: {mail_sender.template}"
        )
        email_service.register_to_db(email_object=email_object, song=song)


if __name__ == "__main__":
    main(song_name)
