MODULE := aws_proxy_integration

LINT = pylint

PYTHON := python3
VENV := .venv
ACTIVATE := . $(VENV)/bin/activate


.PHONY: test
test: lint
	$(ACTIVATE) && coverage run -m pytest && coverage report -m $(MODULE)/*.py

.PHONY: lint
lint: | $(VENV)
	$(ACTIVATE) && $(LINT) $(MODULE)

$(VENV): requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install -r requirements.txt

.PHONY: clean
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf i$(VENV)

