MODULE := aws_proxy_integration

LINT = pylint

PYTHON ?= python3
VENV := .venv
ACTIVATE := . $(VENV)/bin/activate


.PHONY: test
test: lint
	$(ACTIVATE) && coverage run --omit='tests/*,$(VENV)/*,conftest.py' -m pytest -vv && coverage report -m

.PHONY: lint
lint: | $(VENV)
	$(ACTIVATE) && $(LINT) $(MODULE)

$(VENV): requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install -r requirements.txt

################################################################################
# Clean the workspace
################################################################################
.PHONY: clean
clean: clean-venv clean-python clean-test

# Remove the Python virtual environment
.PHONY: clean-venv
clean-venv:
	rm -rf $(VENV)

# Remove the Python cruft
.PHONY: clean-python
clean-python:
	find . -type d -name __pycache__ -exec rm -r {} \+
	find . -type f -name "*.py[c|o]" -exec rm {} \+

# Remove the testing files
.PHONY: clean-test
clean-test:
	rm .coverage
	rm -rf .pytest_cache
