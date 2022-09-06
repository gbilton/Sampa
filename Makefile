api:
	uvicorn app.main:app --reload

send:
	python -m app.emails.send_email

test:
	python -m app.emails.send_test_email

import: 
	python -m app.importer

generate:
	python -m app.exporter

review:
	alembic revision --autogenerate

upgrade:
	alembic upgrade head