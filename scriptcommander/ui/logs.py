import click
import random

from scriptcommander.database import DatabaseLayer
from scriptcommander.settings import CONF_KEY_CHARS, CONF_KEY_LENGTH

# Helper Functions
def confirm_deletion(log_count):
    confkey = "".join(random.choices(CONF_KEY_CHARS, k=CONF_KEY_LENGTH))
    click.echo(f"{log_count} entries staged for deletion. Type the following to confirm: {confkey}")
    value = click.prompt(">", type=str)
    if confkey != value:
        click.echo("Incorrect value. Aborting.")
        return False
    return True

@click.group()
def logs():
    """Subcommand: Manage logs."""
    pass


@logs.command()
@click.argument('script_hash', required=False)
@click.option("-l", "--level")
def show(script_hash, level):
    """Show logs. Optionally, specify a script and/or log-level"""
    # Check if an int is passed as a str
    try:
        level = int(level)
    except:
        pass
    logs = DatabaseLayer().get_logs(script_hash = script_hash, level=level)
    for log in logs:
        click.echo(f"{log['alert_time'].split('.')[0]} | {log['script_hash']} | {log['level']: <8} | {log['text']}")


@logs.command()
@click.argument('script_hash', required=False)
@click.option("-l", "--level")
def delete(script_hash, level):
    """Delete log entries. Optionally, specify a script and/or log-level.
       Logs with a lower level get removed as well."""
    log_count = len(DatabaseLayer().del_logs_staging(script_hash, level))
    if confirm_deletion(log_count):
        DatabaseLayer().del_logs(script_hash, level)
        click.echo(f"Deleting {log_count} logs")

