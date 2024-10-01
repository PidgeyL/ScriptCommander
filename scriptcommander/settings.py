import os
import string

# Folder Functions
def from_project_dir(*args):
    return os.path.normpath( os.path.join(_project_dir, *args) )

def from_config_dir(*args):
    return os.path.normpath( os.path.join(config_dir, *args) )

# Private vars
_project_dir  = os.path.join( os.path.dirname(os.path.realpath(__file__)), ".." )
_current_user = os.path.expanduser("~")

# Public Constants
CONF_KEY_LENGTH = 6 # Length of a generated set of characters to confirm
CONF_KEY_CHARS  = string.digits

# Public vars
config_dir    = os.path.join(_current_user, ".config", "scriptcommander")
database_file = from_config_dir('sc.db')
script_dir    = from_config_dir('scripts')
