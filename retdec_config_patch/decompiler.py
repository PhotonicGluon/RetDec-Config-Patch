# IMPORTS
import glob
import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from time import sleep
from typing import List, Optional

from filelock import FileLock

from retdec_config_patch.config import Config
from retdec_config_patch.misc import gen_random_string, get_hash_of_file
from retdec_config_patch.paths import get_retdec_decompiler_config_path, get_retdec_share_folder

# CONSTANTS
GENERAL_LOCK_FILE_BASE_NAME = "retdec-config-patch.lock"

SPECIFIC_LOCK_FILE_BASE_NAME = "rcp"

ACQUISITION_LOCK_BASE_NAME = "rcp-acquire-lock"
ACQUISITION_LOCK_POLLING_INTERVAL = 0.25


# CLASSES
class Decompiler:
    """
    Class that handles the interactions with the original, unpatched `retdec-decompiler`.
    """

    def __init__(self):
        """
        Initializes a new decompiler.
        """

        self.__is_context_manager = False

        self.parser = ArgumentParser(add_help=False)
        self.parser.add_argument("INPUT_FILE", nargs="?", default=None)

        self.args = {}
        self.retdec_args = [("", "INPUT_FILE")]

        self._add_args()
        self._parse_args()

        self.config = Config.load()
        self.retdec_binary = self.config.retdec_binary

        self.general_retdec_lock = FileLock(os.path.join(get_retdec_share_folder(), GENERAL_LOCK_FILE_BASE_NAME))
        self.lock_id = gen_random_string()
        self.decompiler_config_hash = None
        self.specific_retdec_lock = None

    # Magic methods
    def __enter__(self):
        self.__is_context_manager = True
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Free the specific lock first
        print("---> EXITING SPECIFIC LOCK", self.specific_retdec_lock, self.decompiler_config_hash)
        if self.specific_retdec_lock:
            self.specific_retdec_lock.release()
            print("---> FREED SPECIFIC LOCK", self.specific_retdec_lock.lock_file)
            try:
                os.remove(self.specific_retdec_lock.lock_file)
            except FileNotFoundError:
                pass
            print("---> DELETED SPECIFIC LOCK", self.specific_retdec_lock.lock_file)

        # import time; time.sleep(1)

        # If no more specific locks, free the general lock
        specific_locks = self._get_specific_lock_files()
        print("---> WHATS LEFT", specific_locks)
        if len(specific_locks) == 0:
            print("---> NO MORE SPECIFIC LOCKS", self.decompiler_config_hash)
            self.general_retdec_lock.release()
            print("---> RELEASED GENERAL LOCK")
            try:
                os.remove(self.general_retdec_lock.lock_file)
            except FileNotFoundError:
                pass
            print("---> DELETED GENERAL LOCK")

        self.__is_context_manager = False

    # Helper methods
    def _add_args(self):
        """
        Adds custom arguments to the parser.
        """

        self.parser.add_argument("--help", "-h", action="store_true", help="Show this help.")
        self.parser.add_argument("--config", help="Specify JSON decompilation configuration file.")

    def _parse_args(self):
        """
        Parses all the arguments that are provided to the decompiler.
        """

        _, unknown = self.parser.parse_known_args()

        for arg in unknown:
            if arg.startswith(("-", "--")):
                arg_flag = arg.split("=")[0]
                arg_name = arg_flag.removeprefix("-").removeprefix("-")  # Removes either "-" or "--"
                dashes = arg_flag.removesuffix(arg_name)

                arg_name = arg_name.replace("-", "_")

                self.parser.add_argument(arg_flag, nargs="?")
                self.retdec_args.append((dashes, arg_name))

        args = self.parser.parse_args()
        for key, val in args._get_kwargs():
            self.args[key] = val

    def _show_help(self):
        """
        Show RetDec decompiler help.
        """

        # Get the original help text
        output = subprocess.run([self.retdec_binary, "--help"], capture_output=True)
        help_text = output.stdout.decode().strip()

        # Unfortunately the first line is now wrong, we need to replace it
        help_lines = help_text.split("\n")
        help_lines[0] = "Patched `retdec-decompiler`:"
        help_text = "\n".join(help_lines)

        # Output the help text
        print(help_text)

    def _generate_lock_file_path(self, hash: str) -> os.PathLike[str]:
        """
        Generates the path to the lock file.

        :param hash: hash of the config file
        :returns: path to the lock file
        """

        return os.path.join(get_retdec_share_folder(), f"{SPECIFIC_LOCK_FILE_BASE_NAME}-{hash}-{self.lock_id}.lock")

    def _generate_acquisition_file_path(self, hash: str) -> os.PathLike[str]:
        """
        Generates the path to the file that signals that the config with the given hash is waiting to acquire the general lock.

        :param hash: hash of the config file
        :return: file path
        """

        return os.path.join(get_retdec_share_folder(), f"{ACQUISITION_LOCK_BASE_NAME}-{hash}.lock")

    def _get_specific_lock_files(self) -> List[os.PathLike[str]]:
        """
        Returns a list of the specific lock file paths.
        """
        return list(
            glob.glob(
                os.path.join(
                    get_retdec_share_folder(), f"{SPECIFIC_LOCK_FILE_BASE_NAME}-{self.decompiler_config_hash}-*.lock"
                )
            )
        )

    def _use_config_file(self, config_file: os.PathLike[str]):
        """
        Sets up the RetDec directory to properly use the configuration file specified.

        :param config_file: path to the configuration file
        """

        # Check if the config that we want to use is the same as the one replaced
        existing_config = get_retdec_decompiler_config_path()

        self.decompiler_config_hash = get_hash_of_file(config_file)
        existing_hash = get_hash_of_file(existing_config)

        # Increment the lock number until we get a new lock
        while os.path.exists(self._generate_lock_file_path(self.decompiler_config_hash)):
            self.lock_id = gen_random_string()

        # Get the lock specific to the current config
        self.specific_retdec_lock = FileLock(self._generate_lock_file_path(self.decompiler_config_hash))
        self.specific_retdec_lock.acquire()

        # If we are using an existing config, that's all that needs to be done
        if self.decompiler_config_hash == existing_hash:
            return

        # If the two configs differ, we need to acquire the general lock
        acquisition_file_path = self._generate_acquisition_file_path(self.decompiler_config_hash)
        if os.path.isfile(acquisition_file_path):
            # Wait for acquisition
            print("===> AWAITING ACQUIRING GENERAL LOCK", self.decompiler_config_hash)
            while os.path.isfile(self._generate_acquisition_file_path(self.decompiler_config_hash)):
                sleep(ACQUISITION_LOCK_POLLING_INTERVAL)
            print("===> WAIT OVER", self.decompiler_config_hash)
            return

        # This process claims responsibility for acquiring the general lock on behalf of that config file
        with open(acquisition_file_path, "w"):
            pass

        print("===> ACQUIRING GENERAL LOCK", self.decompiler_config_hash)
        self.general_retdec_lock.acquire()
        print(os.listdir(get_retdec_share_folder()))
        print("===> ACQUIRED GENERAL LOCK", self.decompiler_config_hash)

        os.remove(acquisition_file_path)

        # Rename the existing configuration file
        renamed_old_config = existing_config + "-old"
        os.rename(existing_config, renamed_old_config)

        # Copy the config file into the share folder
        shutil.copy(config_file, existing_config)

    def _revert_config_file(self):
        """
        Reverts the config file back to how it was.
        """

        # Check if any processes are still using the lock file
        specific_lock_files = self._get_specific_lock_files()
        if len(specific_lock_files) > 1:  # Not just this process
            # Don't revert config
            return

        # Otherwise, revert the configuration file
        print("===> REVERTING CONFIG FILE")
        config_file = get_retdec_decompiler_config_path()
        old_config = config_file + "-old"

        os.remove(config_file)
        os.rename(old_config, config_file)

        print("===> REVERTED")

    # Public methods
    def execute(self):
        """
        Run the decompiler with the given arguments.

        :raises Exception: if the decompiler is not being run within a `with` block
        """

        # Check that this is being run in a context
        if not self.__is_context_manager:
            raise Exception("The decompiler class should only be used with `with`")

        # Check if any of the patched arguments are provided
        if self.args.get("help"):
            self._show_help()
            return

        config_file = self.args.get("config")
        if config_file:
            if not os.path.isfile(config_file):
                print(f"No config file can be found at '{config_file}'.")
                sys.exit(1)
            self._use_config_file(config_file)

        # Keep only the normal arguments
        retdec_options = {}
        for dashes, arg in self.retdec_args:
            retdec_options[dashes + arg] = self.args[arg]

        # `INPUT_FILE` has to be a provided positional argument for the original `retdec-decompiler`
        input_file = retdec_options["INPUT_FILE"]
        del retdec_options["INPUT_FILE"]

        # Form the retdec command
        command = [self.retdec_binary]
        if input_file is not None:
            command.append(input_file)

        for key, val in retdec_options.items():
            command.append(key)
            if val is not None:
                command.append(val)

        try:
            # TODO: REMOVE
            import time, random

            print("SLEEP START")
            time.sleep(random.randint(0, 3) + 0.5)
            print("SLEEP END")

            subprocess.run(command)
        finally:
            # Reset configuration file
            if config_file:
                self._revert_config_file()
