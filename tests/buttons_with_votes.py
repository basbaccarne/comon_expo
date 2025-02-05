# This script reads the state of three buttons connected to GPIO pins 4, 14 and 25
# These are votes that are stored in a json file

import json
from time import sleep
from gpiozero import Button
from sys import exit
from pathlib import Path

# change filename to start a new campaign
active_campaign = "votes_test.json"

# GPIO button setup
# buttons are connected to ground and pins 4, 14 and 25
button1 = Button(4)
button2 = Button(14)
button3 = Button(25)

# PATHS
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / 'data'
VOTE_FILE = DATA_DIR / active_campaign

# Load previous votes if available
def load_votes():
    try:
        with open(VOTE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"button1": 0, "button2": 0, "button3": 0}

# Save vote counts to file
def save_votes(votes):
    with open(VOTE_FILE, 'w') as file:
        json.dump(votes, file)

# Initialize vote counts
votes = load_votes()
print("Current votes:", votes)

try:
    while True:
        if button1.is_pressed:
            votes["button1"] += 1
            print("Button 1 pressed.")
            print("Total votes: [1] ", votes["button1"], " || [2] ", votes["button2"], " || [3] ", votes["button3"])
            save_votes(votes)
            sleep(0.3)  # Debounce
        if button2.is_pressed:
            votes["button2"] += 1
            print("Button 2 pressed.")
            print("Total votes: [1] ", votes["button1"], " || [2] ", votes["button2"], " || [3] ", votes["button3"])
            save_votes(votes)
            sleep(0.3)
        if button3.is_pressed:
            votes["button3"] += 1
            print("Button 3 pressed.")
            print("Total votes: [1] ", votes["button1"], " || [2] ", votes["button2"], " || [3] ", votes["button3"])
            save_votes(votes)
            sleep(0.3)
except KeyboardInterrupt:
    print("\nExiting program...")
    exit()
