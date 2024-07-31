import click

from scriptcommander.database import DatabaseLayer

@click.group()
def settings():
    """Subcommand: Manage settings."""
    pass


@settings.command()
@click.argument('setting')
@click.argument('value', required=False)
def set(setting, value):
    """Set setting"""
    if not value:
        value = click.prompt(f'Set "{setting}" to? =>', type=str)
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
