run:
	uvicorn app.main:app --reload

send:
	python -m app.emails.send_email

import: 
	python -m app.importer

generate:
	python -m app.exporter