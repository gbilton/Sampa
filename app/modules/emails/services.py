from app.modules.emails.models import EmailAddress


class EmailService:
    @classmethod
    def get_email(cls, session, email_address: str):
        email = session.query(EmailAddress).filter_by(address=email_address).first()
        if not email:
            raise Exception("No email found!")
        return email
