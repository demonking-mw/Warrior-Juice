# Warrior-Juice

Rules:

python: mandatory type hint, string for complex type
python: mandatory comment for functions and classes

mandatory comment for dataclasses and any data definition, something like racket data def.
Before pushing anything on backend, go to backend and run "black ." in terminal without ""


Backend setup: 
1. cd to Warrior-Juice
2. venv activate
3. pip install -r requirements.txt
4. make an .env file under Warrior-Juice
5. Ask for what to put in it
6. run the API and run tests if desired
7. cook!


venv activate:
.\venv\Scripts\Activate.ps1

Run API:
python -m backend.flask_api.api_1

Test: 
python -m backend.flask_api.test


On WSL (Linux):

git config --global core.autocrlf input
This keeps files as LF when committing but leaves the working directory unchanged (always LF).

On Windows:

git config --global core.autocrlf true
This converts LF to CRLF on checkout and back to LF on commit.

On Mac:
Run the following commands for the best setup:

git config --global core.autocrlf input


Test script: for any tests ran, if it is successful, return an exit code of 0.

If something is cooked in the tests, return an exit code of 3 because Mini picked 3.
DO NOT THROW ERROR PLEASEEEEEEEEEE



Testing: 
1. be in repo root directory
2. ./testScripts/test_api.sh xxx
3. replace xxx with the test sets you want to complete, an example is simple
4. ignore the .txt suffix