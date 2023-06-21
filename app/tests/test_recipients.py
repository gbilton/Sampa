import pytest
from app.db.database import get_db
from app.emails.mail import EmailParser, EmailService, EmailTemplateEnum
from app.modules.genres.services import GenreService
from app.modules.songs.models import Song
from app.modules.songs.schemas import SongGenreEnum
from app.modules.songs.services import SongService


@pytest.fixture(scope="session")
def session():
    return next(get_db())


@pytest.fixture(scope="session")
def song(session):
    song_name = "Savage"
    song = SongService.get_song(session, song_name)
    return song


@pytest.fixture(scope="session")
def recipients(session, song):
    all_genre = GenreService.get_genre(session, SongGenreEnum.all_genre)
    template = EmailTemplateEnum.rampak_template
    email_parser = EmailParser(template)
    recipients = email_parser.get_recipients(
        song=song, all_genre_contacts=all_genre.contacts
    )
    return recipients


def test_song_in_db(song):
    assert isinstance(song, Song)


def test_song_has_link(song):
    assert song.link is not None
    assert isinstance(song.link, str)


def test_recipient_unique_emails(recipients):
    """check if emails are unique"""
    assert len(recipients) == len(set(recipients))


def test_recipient_genres(session, recipients, song):
    """check if genres are same as song and all genres"""
    email_service = EmailService()
    for recipient in recipients:
        email = email_service.get_email_object(session, recipient)
        contact = email.contact
        contact_genres = [genre.name for genre in contact.genres]
        song_genres = [genre.name for genre in song.genres]

        has_common_genre = any(genre in contact_genres for genre in song_genres)
        has_all_genre = SongGenreEnum.all_genre in contact_genres

        assert has_common_genre or has_all_genre


def test_recipient_command(session, recipients):
    """check if command is emailing"""
    email_service = EmailService()
    for recipient in recipients:
        email = email_service.get_email_object(session, recipient)
        command = email.command.name
        assert command == "Emailing"
