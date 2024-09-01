import click

from scriptcommander.database import DatabaseLayer

@click.group()
def logs():
    """Subcommand: Manage logs."""
    pass


@logs.command()
@click.argument('script_hash', required=False)
def show(script_hash):
    """Show logs. Optionally, specify a script."""
    logs = DatabaseLayer().get_logs(script_hash = script_hash)
    for log in logs:
        click.echo(f"{log['alert_time'].split('.')[0]} | {log['script_hash']} | {log['level']: <8} | {log['text']}")
