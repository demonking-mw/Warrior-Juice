#!/bin/bash

# Must be ran at the repo root

# Takes one input, which is the file name of the test suite to run.
if [ ${#} -ne 1 ]; then
    echo "Usage: $0 suite-file program" >&2
    exit 1
fi

VENV_PATH="./venv"  # Change this if your venv is in a different location

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

test_file="./backend/api_tests/$1.txt"

if [ ! -f "$test_file" ]; then
    echo "Error: Test suite file not found: $1" >&2
    exit 1
fi

# Run the test program
python -m backend.flask_api.api_1 &
echo "Running api server"
sleep 12 # Wait for the server to start

for test_file in $(cat $test_file); do
    python -m backend.api_tests."$test_file"
    if [ $? -eq 0 ]; then
        echo "Test $test_file passed"
    else
        echo "Test $test_file failed"
    fi
done


pkill -f "backend.flask_api.api_1"
exit 0


