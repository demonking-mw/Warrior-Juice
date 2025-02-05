# Warrior-Juice
Style Rules: for sample thing

folder names:
sample_thing

file names:
sameple_thing

python: main classes: same as file name
SampleThing

functions:
sample_thing

variables: 
sample_thing

constants:
SAMPLE_THING




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

bash
Copy
Edit
git config --global core.autocrlf input
This keeps files as LF when committing but leaves the working directory unchanged (always LF).

On Windows (for your collaborators):

bash
Copy
Edit
git config --global core.autocrlf true
This converts LF to CRLF on checkout and back to LF on commit.