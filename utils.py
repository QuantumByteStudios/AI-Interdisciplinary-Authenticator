import json
import sqlite3
import os
import sys
import subprocess


class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RED = '\u001b[31m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def clear_screen():
    # For Windows
    if os.name == 'nt':
        subprocess.run("cls", shell=True)
    # For Linux and macOS
    else:
        subprocess.run("clear", shell=True)


def aiInterdisciplinaryAuth(prompt):

    NEGATIVE = {"prompt": prompt, "status": "NEGATIVE"}
    POSITIVE = {"prompt": prompt, "status": "POSITIVE"}

    prompt = prompt.lower()
    # prompt = prompt.split()
    # print(prompt)

    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor()

    # Check if the 'prompts' table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='prompts'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute(
            f"SELECT * FROM prompts WHERE prompt = '{prompt}'")
        row = cursor.fetchone()
        # print(row)
        if row == None:
            return POSITIVE
        else:
            return NEGATIVE
    return POSITIVE


def askLlama(message):
    # Variables
    model = "llama2-uncensored"
    head = f"curl http://localhost:11434/api/generate -d"
    tail = ' \'{"model": "'+model+'", "prompt": "'+message+'"}\''
    command = head + " " + tail
    # print("Command: " + command) # Debugging

    # Send Request to the local server
    output = subprocess.check_output(command, shell=True)
    result = output.decode('utf-8')
    # print(result) # Debugging

    # Fetch "Response" from each line of a string
    words = []
    for line in result.split("\n"):
        if "response" in line:
            tempJson = json.loads(line)
            word = tempJson['response']
            words.append(word)

    response = "".join(words)

    # # # PRINTING THE RESPONSE
    # # Clear the terminal
    # subprocess.run("clear", shell=True)
    # # Print word by word with a little delay :)
    # for word in words:
    #     print(word, end='', flush=True)
    #     sys.stdout.flush()
    #     subprocess.run("sleep 0.1", shell=True)
    # print("\n")

    return response
