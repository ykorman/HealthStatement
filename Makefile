export

SHELL := /bin/bash
FLASK_ENV ?= development

run:
	source ./env/bin/activate && flask run