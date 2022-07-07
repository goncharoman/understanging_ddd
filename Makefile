# GLOBALS
VENV_PATH=./.venv/bin


.DEFAULT_GOAL := help


# INSTALL (via poetry)
.PHONY: install
install: poetry-install  ## Install dependencies (via poetry)

poetry-install:
	@echo "* Install dependencies"
	@if command -v poetry &> /dev/null ; then \
		poetry install; \
	else \
		echo "- No found: poetry, skipping"; \
	fi

.PHONY: static
static:  ## Generate static
	@echo "* Generate static files"
	@$(VENV_PATH)/python manage.py collectstatic --no-input

.PHONY: translate
translate:  ## Generate translate files
	@echo "* Generate translate files"
	@$(VENV_PATH)/python manage.py compilemessages 

# LINTING
.PHONY: lint
lint:  ## Run linting
	@echo "* Running linting"
	@$(VENV_PATH)/python -m flake8 server

# FORMAT
.PHONY: format
format:  ## Run formatter
	@echo "* Running format"
	@$(VENV_PATH)/python -m isort --diff
	@$(VENV_PATH)/python -m autopep8

# TESTS
.PHONY: tests
tests:  ## Run tests
	@echo "* Running tests"
	@$(VENV_PATH)/python -m pytest

# HELP
PHONY: help
help:  ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
