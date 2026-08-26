import json

output = ['']

# Gets the "base_path" variable passed in by RunPy
base_path = globals().get("base_path")

# Opens the commands list
# NOTE: I could and probably should pass the commands list through "main.py"
with open(base_path / "System/Commands.json") as cmds_file:
    raw_cmds = json.load(cmds_file)
cmds = raw_cmds["commands"]

# Loops through each command
for cmd in cmds:
    saved_cmd = cmds[cmd]

    # Adds the name and description of the command if it's queryable
    if saved_cmd['CanQuery'] == "True":
        name = saved_cmd['name']
        disc = saved_cmd['disc']

        output.append(f'\n{name} - {disc}')
    continue

print(" ".join(output))
