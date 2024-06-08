# IMPORTS
import os
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
    return Path(path).parent.parent.absolute()  # Need to use `.parent` twice as the first time just gets the bin folder


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


# DEBUG CODE
if __name__ == "__main__":
    print(get_retdec_folder())
    print(get_retdec_share_folder())
