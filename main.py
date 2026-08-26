import json
import os
import runpy
import sys
import time
from pathlib import Path

import colorama
from argon2 import PasswordHasher
from colorama import Fore

import Utillities
from System import Accounts

colorama.init(autoreset=True)

base_path = Path(__file__).resolve().parent

print("Initializing system arrays")

with open(base_path / "System/OsInfo.json") as osi:
  raw_osinfo = json.load(osi)
osinfo = raw_osinfo['Info']
print("Loaded OS Info")

with open(base_path / "System/Commands.json") as cmdl:
  raw_cmd_list = json.load(cmdl)
cmd_list = raw_cmd_list['commands']
print("Loaded command list")

with open(base_path / "System/Users.json") as accl:
  raw_account_list = json.load(accl)
account_list = raw_account_list['Users']

print("Initializing system variables")

os.environ["TERM"] = "xterm-256color"

osname = osinfo['Name']
osversion = osinfo['Version']

input_prefix = f"{Fore.LIGHTGREEN_EX}@{osname}{Fore.WHITE}$ "

ph = PasswordHasher()

Utillities.clear()

print("Initializing system functions")

def main(username, baseinputtext, cmdlist):
  Utillities.clear()
  welcome_message = Fore.BLUE + "Welcome to "+Fore.CYAN+osname+Fore.BLUE+" "+\
  osversion+"!\nFun Fact: NOT IMPLEMENTED"
  
  print(welcome_message)
  
  while True:
    # Initializes the user input variable
    cmd_input = input(Fore.GREEN + username + Fore.WHITE + baseinputtext)
    
    # Split the input to separate command and arguments
    input_parts = cmd_input.split(' ', )
    base_command = input_parts[0]

    if base_command in cmdlist:
      current_command = cmdlist[base_command]
      
      # Check if command requires an argument
      if current_command['HasArg'] == "True":
        if not len(input_parts) > 1:
          print(f"Command '{cmd_input}' requires an argument")
          continue
      # Execute the command
      cmd = base_path / current_command['exec']
      runpy.run_path(cmd, init_globals={"args": input_parts, "base_path": base_path})
    else:
      print("Invalid command, type help for a list of commands")
def login_screen():
  Utillities.clear()

  login_input = input("Login-in(l) or Create(c)")

  username_input = input("Username: ")
  password_input = input("Password: ")

  if login_input.lower() == "l":
    try:
      Accounts.login(ph, account_list, username_input, password_input)
      main(username_input, input_prefix, cmd_list)
    except (Accounts.UserNotFoundError, Accounts.InvalidPasswordError): # Pretty self-explanatory, it prints an alert and exits.
      print("Wrong username or password,\nShutting down")
      time.sleep(2.5)
      sys.exit()
  elif login_input.lower() == "c":
    try:
      new_account_list: dict = Accounts.create(ph, raw_account_list, username_input, password_input)

      with open(base_path / "System/Users.json", 'w') as f:
        json.dump(new_account_list, f, indent=2)

      main(username_input, input_prefix, cmd_list)
    except Accounts.UserAlreadyExistsError:
      print("User already exists, returning to logon screen")
      time.sleep(2.5)
      login_screen()
Utillities.clear()

print("Loading... ")

login_screen()