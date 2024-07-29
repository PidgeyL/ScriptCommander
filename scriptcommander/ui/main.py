import click

from scriptcommander.ui.functions import interact_reload_scripts, list_enabled_scripts
from scriptcommander.ui.functions import list_disabled_scripts,   set_status_script
from scriptcommander.scripts      import ScriptManager
from scriptcommander.database     import DatabaseLayer

# Define the main group of commands
@click.group()
def manager():
    pass

###
# Scripts
###
@manager.group()
def scripts():
    """Subcommand: Manage scripts."""
    pass

# Scan the scripts folder for changes
@scripts.command()
def reload():
    """Scan for available scripts."""
    interact_reload_scripts()

# List scripts
@scripts.command()
@click.argument('_type', required=False)
def list(_type):
    """List plugins."""
    if not _type: _type = ""
    if _type.lower() in ['enabled', ""]:
        list_enabled_scripts()
    if _type.lower() in ['disabled', ""]:
        list_disabled_scripts()
    if _type.lower() not in ['enabled', 'disabled', '']:
        click.echo("Valid types: enabled, disabled")

# Enable a script
@scripts.command()
@click.argument('script_hash')
def enable(script_hash):
    """Enable a specific script."""
    set_status_script(script_hash, True)

# Disable a script
@scripts.command()
@click.argument('script_hash')
def disable(script_hash):
    """Disable a specific script."""
    set_status_script(script_hash, False)

###
# Settings
###
@manager.group()
def settings():
    """Subcommand: Manage settings."""
    pass

# Set / update a setting
@settings.command()
@click.argument('setting')
@click.argument('value', required=False)
def set(setting, value):
    """Set setting"""
    if not value:
        value = click.prompt(f'Set "{setting}" to? =>', type=str)
    DatabaseLayer().set_setting(setting, value)

# Delete a setting
@settings.command()
@click.argument('setting')
def delete(setting):
    """Delete setting"""
    DatabaseLayer().del_setting(setting)

# Delete a setting
@settings.command()
def list():
    """List settings"""
    click.echo("\n".join(DatabaseLayer().list_settings()))


###
# Run Scripts
###
# Running enabled scripts
@manager.command()
def run():
    """Run all scripts."""
    sm = ScriptManager()
    sm.run_scripts()

###
# Logs
###
# Show logs
@manager.command()
@click.argument('script_hash', required=False)
def logs(script_hash):
    """Show logs. Optionally, specify a script."""
    if script_hash:
        click.echo(f"Showing logs for script: {script_hash}")
    else:
        click.echo("Showing all logs...")


# Entry point
if __name__ == '__main__':
    manager()
