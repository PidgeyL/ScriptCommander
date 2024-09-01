import click

from scriptcommander.database import DatabaseLayer

@click.group()
def settings():
    """Subcommand: Manage settings."""
    pass


@settings.command()
@click.argument('setting')
@click.argument('value', required=False)
+@click.option("-b", "--boolean", is_flag=True)
def set(setting, value, boolean):
    """Set setting"""
    if not value:
        value = click.prompt(f'Set "{setting}" to? =>', type=str)
    if boolean:
        if   value.lower() in ['true',  'yes', 'on',  'enable',  'enabled']:
            value = "1"
        elif value.lower() in ['false', 'no',  'off', 'disable', 'disabled']:
            value = "0"
        else:
            click.echo(f"'{value}' is not a valid boolean value.")
    DatabaseLayer().set_setting(setting, value)


@settings.command()
@click.argument('setting')
def delete(setting):
    """Delete setting"""
    DatabaseLayer().del_setting(setting)


@settings.command()
def list():
    """List settings"""
    click.echo("\n".join(DatabaseLayer().list_settings()))
