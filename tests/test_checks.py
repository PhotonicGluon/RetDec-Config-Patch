# IMPORTS
import os

import pytest

from retdec_config_patch.checks import (
    is_config_file_editable,
    is_patcher_available_globally,
    is_retdec_available,
    is_retdec_share_folder_writable,
    is_retdec_version_compatible,
)
from retdec_config_patch.paths import get_executable_path, get_retdec_decompiler_config_path


# TESTS
def test_is_retdec_available():
    # Initially retdec should be available
    assert is_retdec_available()

    # Get where RetDec is
    old_path = get_executable_path("retdec-decompiler")
    new_path = old_path + "-TEMP"

    # Move it
    os.rename(old_path, new_path)

    # RetDec should now not be available
    assert not is_retdec_available()

    # Making a fake RetDec should also result in an error
    with open(old_path, "w") as f:
        f.write("BLAH")

    assert not is_retdec_available()

    # Revert
    os.remove(old_path)
    os.rename(new_path, old_path)
    assert is_retdec_available()


def test_is_retdec_version_compatible():
    # The executable that we use is compatible
    assert is_retdec_version_compatible()


def test_is_retdec_share_folder_writable():
    # The way we installed RetDec makes the share folder writable
    assert is_retdec_share_folder_writable()


def test_is_config_file_editable():
    # By default the config file is editable
    assert is_config_file_editable()

    # Try (re)moving the config file
    old_path = get_retdec_decompiler_config_path()
    new_path = old_path + "-TEMP"
    os.rename(old_path, new_path)

    with pytest.raises(FileNotFoundError):
        is_config_file_editable()

    # Revert
    os.rename(new_path, old_path)
    assert is_config_file_editable()


def test_is_patcher_available_globally():
    # If installed correctly, this should work
    assert is_patcher_available_globally()
