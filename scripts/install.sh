#!/bin/bash

pyenv install -s # Redirecting stderr in null device
pipenv --clear
if [ -d ".venv" ]; then
    echo "Removing existing .venv"
    pipenv --rm || rm -rf .venv  # Remove .venv manually if pipenv fails to remove it
fi
mkdir -p .venv
pipenv install --dev