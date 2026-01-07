#!/bin/bash

VENV_DIR="labeler-venv"

echo "Make sure you run this code from inside your app folder, where the venv should be created. Press 'y' to begin, or any other key to quit: "
read proceed

if [ "$proceed" == 'y' ]; then
    echo "Commencing setup..."
else
    echo "Exiting."
    exit 0
fi

echo "Creating virtual environment: $VENV_DIR..."
python3 -m venv $VENV_DIR

echo "Activating virtual environment..."
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
    echo "Installing Python packages..."
    pip install -r requirements.txt
    echo "Downloading the spaCy model en_core_web_sm..."
    python3 -m spacy download en_core_web_sm
else
    echo "Error: couldn't find activation script. Please proceed manually."
    exit 1
fi

echo "Deployment complete; virtual environment active."
