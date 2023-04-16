#!/bin/bash

rm -rf .venv
mkdir -p .venv
pyenv install -s # Redirecting stderr in null device
pipenv install
pipenv install --dev