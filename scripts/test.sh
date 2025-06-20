#!/bin/bash

# Handles running unit tests
source "$(pipenv --venv 2>/dev/null)/bin/activate"
python -m pytest \
    --cov=smalldiff \
    --cov-branch \
    --cov-report=term \
    --cov-fail-under=80