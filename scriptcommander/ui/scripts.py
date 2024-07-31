import click

from scriptcommander.scripts      import ScriptManager
from scriptcommander.database     import DatabaseLayer

# Constants
_HASH_LENGTH_ = 8

# Helper Functions
def print_table(data):
    rows = [["HASH", "SCRIPT", "VERSION", "PATH", "ENABLED"]]
    for script in data:
        hash    = script['script_hash']
        name    = script['script_name']
        version = script['script_version']
        path    = script['script_file']
        enabled = script['enabled']
        rows.append([hash, name, version, path, enabled])
    len_hash    = _HASH_LENGTH_
    len_name    = max([len(x[1]) for x in rows])
    len_version = max([len(x[2]) for x in rows])
    len_path    = max([len(x[3]) for x in rows])
    for row in rows:
        click.echo(f"{row[0]: <{len_hash}}   {row[1]: <{len_name}}   {row[2]: <{len_version}}   {row[3]: <{len_path}}    {row[4]}")


def format_entry(script):
    return f"{script['script_name']} {script['script_version']} ({script['script_file']}) [{script['script_hash']}]"


def set_status_script(hash, status):
    dbl     = DatabaseLayer()
    scripts = [x for x in dbl.get_scripts()]
    _status = "Enabling" if status else "Disabling"

    for script in scripts:
        if script['script_hash'].startswith(hash):
            dbl.set_script_status(script, status)
            click.echo(f"{_status}: {format_entry(script)}")


# Click expansion
@click.group()
def scripts():
    """Subcommand: Manage scripts."""
    pass


@scripts.command()
def reload():
    """Scan for available scripts."""
    sm        = ScriptManager()
    dbl       = DatabaseLayer()
    available = sm.scan_scripts()
    active    = [x for x in dbl.get_scripts() if x['enabled']]

    # Hashes for searching
    active_hashes    = [x['script_hash'] for x in active]
    available_hashes = [x['script_hash'] for x in available]
    # New scripts
    new_scripts   = [x for x in available if x['script_hash'] not in active_hashes]
    unavailable   = [x for x in active    if x['script_hash'] not in available_hashes]
    if len(new_scripts) == 0 and len(unavailable) == 0:
        click.echo("No changes detected")
        return
    # Add new scripts
    if len(new_scripts) >= 1:
        click.echo("[ NEW SCRIPTS DETECTED ]")
        for script in new_scripts:
            click.echo(f" -> {format_entry(script)}")
            if click.confirm("    [?] Import script?"):
                if click.confirm("    [?] Enable script?"):
                    script['enabled'] = True
                else:
                    script['enabled'] = False
                dbl.add_script(script)
    if len(unavailable) >= 1:
        click.echo("[ SCRIPTS NO LONGER AVAILABLE ]")
        for script in unavailable:
            click.echo(f" -> {format_entry(script)}")
            if click.confirm("    [?] Remove script?"):
                click.echo("     -> Script deleted")
                dbl.delete_script(script)
            else:
                click.echo("     -> Script disabled")
                dbl.set_script_status(script, False)


@scripts.command()
@click.argument('_type', required=False)
def list(_type):
    """List scripts."""
    if not _type:
        print_table( DatabaseLayer().get_scripts() )
        return
    if _type.lower() in ['enabled', ""]:
        print_table( [x for x in DatabaseLayer().get_scripts() if x['enabled']] )
    if _type.lower() in ['disabled', ""]:
        print_table( [x for x in DatabaseLayer().get_scripts() if not x['enabled']] )
    if _type.lower() not in ['enabled', 'disabled', '']:
        click.echo("Valid types: enabled, disabled")


@scripts.command()
@click.argument('script_hash')
def enable(script_hash):
    """Enable a specific script."""
    set_status_script(script_hash, True)


@scripts.command()
@click.argument('script_hash')
def disable(script_hash):
    """Disable a specific script."""
    set_status_script(script_hash, False)
