import click

from scriptcommander.database import DatabaseLayer
from scriptcommander.scripts  import ScriptManager


def interact_reload_scripts():
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
            print(script)
            click.echo(f" -> {script['script_name']} {script['script_version']}"
                       f" ({script['script_file']}.py) [{script['script_hash']}]")
            if click.confirm("    [?] Import script?"):
                if click.confirm("    [?] Enable script?"):
                    script['enabled'] = True
                else:
                    script['enabled'] = False
                dbl.add_script(script)
    if len(unavailable) >= 1:
        click.echo("[ SCRIPTS NO LONGER AVAILABLE ]")
        for script in unavailable:
            click.echo(f" -> {script['script_name']} {script['script_version']}"
                       f" ({script['script_file']}) [{script['script_hash'][:7]}]")
            if click.confirm("    [?] Remove script?"):
                click.echo("     -> Script deleted")
                dbl.delete_script(script)
            else:
                click.echo("     -> Script disabled")
                dbl.set_script_status(script, False)


def list_enabled_scripts():
    dbl = DatabaseLayer()
    click.echo("[ ENABLED SCRIPTS ]")
    for script in [x for x in dbl.get_scripts() if x['enabled']]:
        click.echo(f" -> {script['script_name']} {script['script_version']}"
                   f" ({script['script_file']}) [{script['script_hash'][:7]}]")

def list_disabled_scripts():
    dbl = DatabaseLayer()
    click.echo("[ DISABLED SCRIPTS ]")
    for script in [x for x in dbl.get_scripts() if not x['enabled']]:
        click.echo(f" -> {script['script_name']} {script['script_version']}"
                   f" ({script['script_file']}) [{script['script_hash'][:7]}]")

def set_status_script(hash, status):
    dbl     = DatabaseLayer()
    scripts = [x for x in dbl.get_scripts()]
    _status = "Enabling" if status else "Disabling"

    for script in scripts:
        if script['script_hash'].startswith(hash):
            dbl.set_script_status(script, status)
            click.echo(f"{_status}: {script['script_name']} {script['script_version']}"
                       f" [{script['script_hash'][:7]}]")
