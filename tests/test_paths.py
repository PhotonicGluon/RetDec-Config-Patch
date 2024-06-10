# IMPORTS
import os

import pytest
from retdec_config_patch.paths import (
    get_executable_path,
    get_retdec_decompiler_config_path,
    get_retdec_folder,
    get_retdec_share_folder,
)


# CONSTANTS
RETDEC_PATH_OLD = get_executable_path("retdec-decompiler")
RETDEC_PATH_NEW = RETDEC_PATH_OLD + "-TEMP"


# TESTS
def test_get_executable_path():
    import sys

    if sys.platform not in {"linux", "linux2", "macos"}:
        print("Not running `get_executable_path()` test.")
        return

    assert get_executable_path("echo") == "/usr/bin/echo"
    with pytest.raises(FileNotFoundError):
        get_executable_path("fake-file")


def test_get_retdec_folder():
    assert os.path.isfile(os.path.join(get_retdec_folder(), "bin", "retdec-decompiler"))

    os.rename(RETDEC_PATH_OLD, RETDEC_PATH_NEW)
    with pytest.raises(FileNotFoundError):
        get_retdec_folder()

    os.rename(RETDEC_PATH_NEW, RETDEC_PATH_OLD)
    assert os.path.isfile(os.path.join(get_retdec_folder(), "bin", "retdec-decompiler"))


def test_get_retdec_share_folder():
    assert os.path.isdir(get_retdec_share_folder())

    os.rename(RETDEC_PATH_OLD, RETDEC_PATH_NEW)
    with pytest.raises(FileNotFoundError):
        get_retdec_share_folder()

    os.rename(RETDEC_PATH_NEW, RETDEC_PATH_OLD)
    assert os.path.isdir(get_retdec_share_folder())


def test_get_retdec_decompiler_config_path():
    assert os.path.isfile(get_retdec_decompiler_config_path())

    os.rename(RETDEC_PATH_OLD, RETDEC_PATH_NEW)
    with pytest.raises(FileNotFoundError):
        get_retdec_decompiler_config_path()

    os.rename(RETDEC_PATH_NEW, RETDEC_PATH_OLD)
    assert os.path.isfile(get_retdec_decompiler_config_path())
