# IMPORTS
import os
import subprocess

from retdec_config_patch.misc import get_retdec_decompiler_config_path


# FUNCTIONS
def is_retdec_available() -> bool:
    """
    Checks if RetDec is available as an executable on the system PATH.

    :return: True if available and False otherwise
    """

    try:
        output = subprocess.run("retdec-decompiler --version", shell=True, stdout=subprocess.PIPE)
    except FileNotFoundError:
        return False

    return output.returncode == 0


def is_config_file_editable() -> bool:
    """
    Checks if the configuration file that this patch needs to edit is actually editable.

    Assumes that RetDec is installed.

    :raises ModuleNotFoundError: if cannot find `retdec-decompiler`
    :raises FileNotFoundError: if cannot find the decompiler configuration file
    :return: True if editable and False otherwise
    """

    config_file_path = get_retdec_decompiler_config_path()

    # Does the config file exist?
    if not os.path.isfile(config_file_path):
        raise FileNotFoundError("Decompiler config file cannot be found")

    # Can we write to it?
    return os.access(config_file_path, os.W_OK)


# DEBUG CODE
if __name__ == "__main__":
    print(is_retdec_available())
    print(is_config_file_editable())
