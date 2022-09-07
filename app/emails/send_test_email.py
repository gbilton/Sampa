import argparse

from app.emails.send_email import main

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

if __name__ == "__main__":
    recipients = ["guilhermebilton@gmail.com", "rgarrubo@gmail.com", "pakpietro@gmail.com"]
    main(song_name, subject, recipients)
