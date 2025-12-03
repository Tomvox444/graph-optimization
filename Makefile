# Makefile to install requirements, check data, and run main.py

# Variables
PYTHON = python3
PIP = pip3
VENV_DIR = venv
REQUIREMENTS = requirements.txt
MAIN = main.py
DATA = data/input.txt

# Default target
all: venv install check_data run

# Create virtual environment
venv:
	@if [ ! -d $(VENV_DIR) ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "Virtual environment created."; \
	fi

# Install requirements in virtual environment
install: venv
	$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS)

# Check if data file exists
check_data:
	@if [ ! -f $(DATA) ]; then \
		echo "Error: $(DATA) not found."; \
		exit 1; \
	fi

# Run the main script using virtual environment
run: venv
	$(VENV_DIR)/bin/$(PYTHON) $(MAIN)

# Clean (optional, if needed)
clean:
	rm -rf __pycache__ $(VENV_DIR)

.PHONY: all venv install check_data run clean