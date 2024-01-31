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