import click

@click.group()
def logs():
    """Subcommand: Manage logs."""
    pass


@logs.command()
@click.argument('script_hash', required=False)
def show(script_hash):
    """Show logs. Optionally, specify a script."""
    if script_hash:
        click.echo(f"Showing logs for script: {script_hash}")
    else:
        click.echo("Showing all logs...")
