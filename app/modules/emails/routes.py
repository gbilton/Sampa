from fastapi import APIRouter, HTTPException
from app.emails.mail import EmailService

from app.exceptions import NotFound

from typing import Optional


emailing_router = APIRouter()
email_service = EmailService()


@emailing_router.post("/emails/send", response_model=str)
async def send_song(song_name: str, subject=Optional[str]):
    try:
        return email_service.add_song(link, name)
    except NotFound as error:
        raise HTTPException(404, detail=str(error))


@emailing_router.post("/emails/test", response_model=str)
async def send_test(song_name: str, subject=Optional[str]):
    try:
        return email_service.send_song()
    except NotFound as error:
        raise HTTPException(404, detail=str(error))
