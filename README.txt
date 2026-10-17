QueueQuest: Theme Park Strategy Analyser

Requirements:
Python 3.9 or later. Standard libraries only.
No additional packages are required.

Run the program:
Open a terminal in the project folder and enter:
    python main.py

Follow the menu prompts to enter your available time and attractions.
All times are entered in whole minutes.

Run the tests:
    python -m unittest -v

Files:
main.py - Main program.
test_queuequest.py - Automated tests.

Saving:
Option 7 saves inputs to session.json.
Option 8 loads the saved inputs.
Option 9 exports analysis_report.txt.
Both files are stored beside main.py.
Changes are not saved automatically.

Assumptions:
Fixed waiting times, one visit per attraction, additive preference scores.
Walking time, breaks and opening hours are excluded.