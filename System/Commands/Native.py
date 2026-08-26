import subprocess

from colorama import Fore

while True:
    command = input(f"{Fore.LIGHTGREEN_EX}FlopOS@Shell{Fore.WHITE}$ ")
    if command.lower() == "FlopOS":
        break
    else:
        subprocess.call(command, shell=True)