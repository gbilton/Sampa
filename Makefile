run:
	uvicorn app.main:app --reload

send:
	python -m app.emails.send_email