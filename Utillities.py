import os
import subprocess

def clear():
    if os.name.startswith('nt'):
        # Uses "cls" to clear the terminal if the user is on Windows
        subprocess.call('cls', shell=True)
    else:
        # Uses "clear" to clear the terminal if the user isn't on Windows
        subprocess.call('clear', shell=True)