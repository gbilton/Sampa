import argparse
from typing import Optional

from tqdm import tqdm

from app.modules.songs.services import SongService

from .mail import EmailParser, EmailService

parser = argparse.ArgumentParser(description="Send test email.")
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


def main(song_name: str, subject: Optional[str]):
    song = SongService.get_song(song_name)
    song_genres = song.genres
    if not song_genres:
        raise Exception(f"Song {song.name} has no genre.")

    email_service = EmailService()
    email_to_use, password_to_use, template = email_service.get_email_headline(song_genres)
    EMAIL_ADDRESS, EMAIL_PASSWORD = email_service.set_email_headline(email_to_use, password_to_use)

    email_parser = EmailParser(template)

    if not subject:
        subject = email_parser.get_subject(song.name)

    recipients = ["guilhermebilton@gmail.com", "ralie139@gmail.com", "pakpietro@gmail.com"]
    for recipient in tqdm(recipients):
        mail_sender, _ = email_service.compose_email(
            recipient=recipient,
            subject=subject,
            email_template=template,
            song=song,
            email_address=EMAIL_ADDRESS,
            email_password=EMAIL_PASSWORD,
        )
        email_service.send_email(mail_sender)


if __name__ == "__main__":
    main(song_name, subject)
