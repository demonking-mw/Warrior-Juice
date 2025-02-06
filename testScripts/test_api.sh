#!/bin/bash

VENV_PATH="../venv"  # Change this if your venv is in a different location

# Check if venv is already activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -d "$VENV_PATH" ]]; then
        echo "Activating virtual environment..."
        source "$VENV_PATH/bin/activate"
    else
        echo "Error: Virtual environment not found at $VENV_PATH"
        exit 1
    fi
else
    echo "Virtual environment already active."
fi

# Run the test program
python -m backend.flask_api.api_1 &
echo "Running api server"
sleep 12 # Wait for the server to start
echo "Attempt to run test"
echo "Running user_test"
python -m backend.api_tests.user_test  # Replace with your actual test script

pkill -f "backend.flask_api.api_1"
# Deactivate venv after running the test (optional)
