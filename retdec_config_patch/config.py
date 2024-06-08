# IMPORTS
import json
import os
from typing import Dict, Any

# CONSTANTS
CONFIG_FILE = "config.json"


# CLASSES
class Config:
    """
    Class containing configuration options.
    """

    fields = ["retdec_binary"]

    def __init__(self):
        """
        Initializes a blank configuration option object.
        """

        self.retdec_binary: str = None

    # Magic methods
    def __repr__(self) -> str:
        return "<RetDec Configuration>"
    
    def __str__(self) -> str:
        return str(self._serialize())

    # Helper methods
    def _serialize(self) -> Dict[str, Any]:
        """
        Serializes the contents of the configuration file.

        :return: dictionary representing the configuration options
        """

        return {field: getattr(self, field) for field in self.fields}

    def _deserialize(self, config_dict: Dict[str, Any]):
        """
        Sets the configuration options based on the provided dictionary.

        :param config_dict: configuration dictionary
        """

        for key, value in config_dict.items():
            setattr(self, key, value)

    # Public methods
    @classmethod
    def load(cls, filepath: os.PathLike[str] = CONFIG_FILE) -> "Config":
        """
        Loads configuration from a JSON file.

        :param filepath: path to the configuration file
        :return: loaded configuration object
        """

        with open(filepath, "r") as f:
            config_dict = json.load(f)

        config = cls()
        config._deserialize(config_dict)
        return config

    def save(self, filepath: os.PathLike[str] = CONFIG_FILE):
        """
        Saves configuration to a JSON file.

        :param filepath: path to the configuration file
        """

        config_dict = self._serialize()
        with open(filepath, "w") as f:
            json.dump(config_dict, f)


# DEBUG CODE
if __name__ == "__main__":
    try:
        config = Config.load("retdec_config_patch/config.json")
    except FileNotFoundError as e:
        print(e)
        config = Config()
    print(config)
    config.retdec_binary = "testing-1234"
    print(config)
    config.save("retdec_config_patch/config.json")
