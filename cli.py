# IMPORTS
import sys

import click

from retdec_config_patch.checks import is_retdec_available, is_config_file_editable

# COMMANDS
@click.command()
def patch_check():
    """
    Runs checks on the system to see whether the patch would work.
    """

    if not is_retdec_available():
        click.echo("RetDec doesn't seem to be installed. The patch will NOT work.")
        sys.exit(1)
    
    try:
        if not is_config_file_editable():
            from retdec_config_patch.misc import get_retdec_decompiler_config_path
            click.echo("It appears that the decompiler config at")
            click.echo(f"\t{get_retdec_decompiler_config_path()}")
            click.echo("cannot be edited. The patch will NOT work.")
            click.echo("Try changing the permissions of that file and try again.")
            sys.exit(1)
    except FileNotFoundError:
        from retdec_config_patch.misc import get_retdec_decompiler_config_path
        click.echo("Cannot find the decompiler config at")
        click.echo(f"\t{get_retdec_decompiler_config_path()}")
        click.echo("The patch will NOT work.")
        click.echo("Please check your installation.")
        sys.exit(1)
    
    click.echo("All checks complete. The patch SHOULD work.")
