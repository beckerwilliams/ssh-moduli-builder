#!/usr/bin/env python3
from json import (dumps, loads)
from pathlib import PosixPath as Path

# _path_parameters are those properties that become `Path` objects in runtime
# NOTE: Supply ONLY the NAMES - Not the path in which they reside.
#       The Config Directory will always be placed in User's HOME
#
# You can change either _def_dirname or _def_cfgname, Or supply your own config on __init__


_def_dirname: str = '.bw_cfg'
_def_cfgname: str = '.config'

# ________________________________________ (DO NOT MODIFY BELOW) _________________________________
_default_pre_config: tuple = (('config_dir', _def_dirname), ('config_file', _def_cfgname))


def default_config() -> dict:
    """

    :return: JSON Object (No PATH Parameters as Values)
    :rtype: dict
    """
    return dict((name, value) for name, value in _default_pre_config)


def _path_parameters() -> list:
    """

    :return: names of configuration properties to be treated as paths
    :rtype: list
    """
    return [entry[0] for entry in [entry for entry in _default_pre_config]]


def _enable_path_properties(config: dict) -> dict:
    """
    Converts Config Manager File format to Runtime Configuration
    :param config: Runtime Configuration
    :type config: dict
    :return: Configuration in File Format
    :rtype: dict
    """
    new_config = dict()
    for prop in config:
        if prop in _path_parameters():
            if prop == 'config_dir':
                new_config['config_dir'] = Path.home().joinpath(config['config_dir'])
            elif prop == 'config_file':
                new_config['config_file'] = Path.home().joinpath(config['config_dir'], config['config_file'])
        else:
            new_config[prop] = config[prop]
    return new_config


def _disable_path_properties(config: dict) -> dict:
    """
    Converts Runtime Configuration to Configuration Manager File Format

    :param config: Working Directory and Configuration File
    :type config: dict
    :return: String formatted Configuration File (JSON)
    :rtype: dict
    """
    config['config_dir'] = config['config_dir'].name
    config['config_file'] = config['config_file'].name
    return config


class ConfigManager(object):

    @classmethod
    def __init__(cls, config: dict = None) -> None:
        """
        If no config provided, default is created and assigned as `cls.config`

        If a Configuration File corresponding to a config  that exists,
        it will take precedence over the provided configuration dict.

        :param config: Application Configuration Directory and File
        :type config: dict
        """
        if not config:
            config = default_config()

        config_file = Path.home().joinpath(config["config_dir"], config["config_file"])
        if config_file.exists and config_file.is_file():
            cls.config = _enable_path_properties(loads(config_file.read_text()))
        else:
            cls.config = _enable_path_properties(config)
            if not cls.config["config_dir"].exists():
                Path.home().joinpath(cls.config["config_dir"]).mkdir(exist_ok=True)
            # Save Configuration File
            config_file.write_text(dumps(config))
