import click

from scriptcommander.database import DatabaseLayer

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
