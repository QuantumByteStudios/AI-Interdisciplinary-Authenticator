import os

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
        os.system('cls')
    # For Linux and macOS
    else:  
        os.system('clear')


import sqlite3

def aiInterdisciplinaryAuth(prompt):

    NEGATIVE = {"prompt": prompt, "status": "NEGATIVE"}
    POSITIVE = {"prompt": prompt, "status": "POSITIVE"}

    prompt = prompt.lower()
    prompt = prompt.split()

    connection = sqlite3.connect('user_database.db')
    cursor = connection.cursor()

    # Check if the 'prompts' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prompts'")
    table_exists = cursor.fetchone()

    if table_exists:
        for word in prompt:
            cursor.execute(f"SELECT * FROM prompts WHERE prompt LIKE '%{word}%'")
            row = cursor.fetchone()
            # print(row)
            if row == None:
                continue
            else:
                return NEGATIVE
    return POSITIVE

# # Example usage:
# prompt_status = aiInterdisciplinaryAuth("write 10 words short message to jeetu mamtora")
# print(prompt_status)
