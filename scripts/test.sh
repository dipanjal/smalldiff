#!/bin/bash

# Handles running unit tests
source "$(pipenv --venv 2>/dev/null)/bin/activate"
python -m pytest