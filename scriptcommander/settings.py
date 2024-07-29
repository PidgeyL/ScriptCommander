import os


# Folder Functions
def from_project_dir(*args):
    return os.path.normpath( os.path.join(_project_dir, *args) )

def from_config_dir(*args):
    return os.path.normpath( os.path.join(config_dir, *args) )

# Private vars
_project_dir  = os.path.join( os.path.dirname(os.path.realpath(__file__)), ".." )
_current_user = os.path.expanduser("~")

# Public vars
config_dir    = os.path.join(_current_user, ".config", "scriptcommander")
database_file = from_config_dir('sc.db')
script_dir    = from_config_dir('scripts')
