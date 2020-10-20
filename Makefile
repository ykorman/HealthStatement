export

SHELL := /bin/bash
FLASK_ENV ?= development

ENV_VARS = MAIL_SMTP MAIL_USER MAIL_PASSWORD REDIS_URL

run:
	source ./env/bin/activate && heroku local

local_env:
	mv -f .env .env.old
	for v in $(ENV_VARS) ; do \
		heroku config:get -s $$v >> .env ; \
	done

.PHONY: run local_env