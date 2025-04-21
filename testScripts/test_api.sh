#!/bin/bash

# Must be ran at the repo root
touch grass
# Takes one input, which is the file name of the test suite to run.
if [ ${#} -ne 1 ]; then
    echo "Usage: takes 1 argument: stem of test suite txt file" >&2
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
echo "black-ing"
black .

test_file="./backend/api_tests/$1.txt"

if [ ! -f "$test_file" ]; then
    echo "Error: Test suite file not found: $1" >&2
    exit 1
fi

# Run the test program
python -m backend.flask_api.api_1 &
echo "Running api server"
sleep 12 # Wait for the server to start
pass_count=0
fail_count=0
for indiv_test in $(cat $test_file | tr -d '\r'); do
    echo -e "\nAttempt to run test $indiv_test: "
    python -m backend.api_tests."$indiv_test"
    if [ $? -eq 0 ]; then
        echo "Test $indiv_test passed"
        pass_count=$((pass_count + 1))
    else
        echo "Test $indiv_test failed"
        fail_count=$((fail_count + 1))
    fi
done
echo -e "\n\nTests completed. Passed: $pass_count, Failed: $fail_count"
if [ $fail_count -eq 0 ]; then
    echo -e "🌸🎂🎉 Cheers! MW 🎉🎂🌸 \n\n"
fi


pkill -f "backend.flask_api.api_1"
echo "Killed api server\n"
exit $fail_count


