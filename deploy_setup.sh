#!/bin/bash

VENV_DIR = ".labeler-venv"

echo "Creating virtual environment: $VENV_DIR..."
Python3 -m venv $VENV_DIR

echo "Activating virtual environment..."
if [-f "$VENV_DIR/bin/activate"]; then
    source "$VENV_DIR/bin/activate" 
else
    echo "Error: couldn't find activation script. Please proceed manually."
    exit 1
fi

echo "Installing Python packages..."
pip install -r requirements.txt

echo "Downloading the spaCy model en_core_web_sm..."
python -m spacy download en_core_web_sm

echo "Deployment complete; virtual environment active."