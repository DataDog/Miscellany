VENV_NAME := venv
VENV_ACTIVATE := $(VENV_NAME)/bin/activate
PYTHON := $(VENV_NAME)/bin/python
PIP := $(VENV_NAME)/bin/pip
PYTHON_VERSION := 3.10  # Specify the desired Python version

.PHONY: all venv dependencies run

all: run

venv: $(VENV_ACTIVATE)

$(VENV_ACTIVATE):
	python$(PYTHON_VERSION) -m venv $(VENV_NAME)
	@echo "Virtual environment created using Python $(PYTHON_VERSION). Activate it using:"
	@echo "source $(VENV_ACTIVATE)"

dependencies: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: dependencies venv
	$(PYTHON) dbm_setup.py



