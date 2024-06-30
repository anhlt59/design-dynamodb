VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python

setup:
	@python3.12 -m virtualenv $(VENV_DIR)
	@source $(VENV_DIR)/bin/activate
	@pip install poetry && poetry install

install:
	@poetry lock && poetry install

start:
	@$(PYTHON) app.py

test:
	@$(PYTHON) -m pytest tests

.PHONY: setup install start test
