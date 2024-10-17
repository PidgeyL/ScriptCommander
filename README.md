# ScriptCommander
ScriptCommander is a tool to help you manage and run a series of smaller scripts in one go, and log their output.
A usecase for this tool may be to run a series of scripts to pull and/or push data in one go, and log their output.

## Usage
### Scripts
 - `scriptcommander scripts list`: lists all the scripts scripcommander can find
 - `scriptcommander scripts reload`: check the scripts folder for changes & reload scripts
 - `scriptcommander scripts enable`: enable (a) script(s)
 - `scriptcommander scripts disable`: disable (a) script(s)

### Settings
 - `scriptcommander settings list`: list all current settings
 - `scriptcommander settings set`: set a value to a setting
 - `scriptcommander settings delete`: delete a setting

### Logs
 - `scriptcommander logs show`: show the logs of all scripts, or the scripts matching the hash. Allows optional log-level
 - `scriptcommander logs delete`: delete logs, according to their hash and/or log level

### Running scripts
 - `scriptcommander run`: runs all the scripts

## Configuration directory
By default, the script uses your .config folder to host its settings and scripts. You can find these under `~/.config/scriptcommander`.
If you want to run the scripts as a system user, you may want to change this directory.
To do so, you can change the settings folder by making a file called `/etc/scriptcommander`, and add the path of your settings folder in there.
The root directory will need to exist for scriptcommander to use this folder. Subfolders will be created by the program.
