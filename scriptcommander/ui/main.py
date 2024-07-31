import click

from scriptcommander.ui.logs     import logs
from scriptcommander.ui.scripts  import scripts
from scriptcommander.ui.settings import settings

# Define the main group of commands
@click.group()
def manager():
    pass


###
# Run Scripts
###
# Running enabled scripts
@manager.command()
def run():
    """Run all scripts."""
    sm = ScriptManager()
    sm.run_scripts()


manager.add_command(logs)
manager.add_command(scripts)
manager.add_command(settings)

# Entry point
if __name__ == '__main__':
    manager()
