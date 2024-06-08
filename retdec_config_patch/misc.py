# IMPORTS
from sys import platform
import os
import subprocess
import shutil
from pathlib import Path


# FUNCTIONS
def get_retdec_folder() -> os.PathLike[str]:
    """
    Gets the installation folder of RetDec.

    Assumes that RetDec is installed.

    :raises ModuleNotFoundError: if cannot find `retdec-decompiler`
    :return: absolute path to the base folder of RetDec
    """

    path = shutil.which("retdec-decompiler")
    if path is None:
        raise ModuleNotFoundError("Cannot locate `retdec-decompiler` executable")
    return Path(path).parent.parent.absolute()  # Use `.parent` twice as first time gets bin folder only


def get_retdec_share_folder() -> os.PathLike[str]:
    """
    Gets the share folder of the RetDec installation.

    Assumes that RetDec is installed.

    :raises ModuleNotFoundError: if cannot find `retdec-decompiler`
    :return: absolute path to the share folder of RetDec
    """

    base_folder = get_retdec_folder()
    return os.path.join(base_folder, "share", "retdec")


def get_retdec_decompiler_config_path() -> os.PathLike[str]:
    """
    Gets the decompiler config path of the RetDec installation.

    Assumes that RetDec is installed.

    :raises ModuleNotFoundError: if cannot find `retdec-decompiler`
    :return: absolute path to the decompiler config of RetDec
    """

    share_folder = get_retdec_share_folder()
    return os.path.join(share_folder, "decompiler-config.json")


def get_executable_path(executable: str) -> os.PathLike[str]:
    """
    An operating system independent method to get the path to an executable.

    :param executable: name of the executable
    :raises Exception: if the platform is not supported
    :return: path to the executable
    """

    if platform == "darwin" or platform.startswith("linux"):
        # Try the POSIX compatible `command` command
        # (See https://stackoverflow.com/a/677212)
        output = subprocess.run(
            f"command -v {executable}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return output.stdout.decode().strip()  # Remove a possible newline
    elif platform == "win32":
        # TODO: Handle windows case
        return executable
    else:
        raise Exception(f"'{platform}' not supported")


# DEBUG CODE
if __name__ == "__main__":
    print(get_retdec_folder())
    print(get_retdec_share_folder())
    print(get_executable_path("retdec-decompiler"))
