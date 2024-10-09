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


def _fs_delete(directory: Path) -> Path:
    # protected_paths = [
    #     Path.home(),
    #     Path('/'),
    #     Path('/etc'),
    #     Path('/usr'),
    #     Path('/usr/local'),
    #     Path('/usr/local/etc'),
    #     Path('/opt'),
    #     Path('/var'),
    #     Path('/var/local')
    # ]
    # if directory in protected_paths:
    #     raise FileExistsError(f'Innappropriate Directory Path: {directory}')

    if directory.exists():
        for file in directory.iterdir():
            if file.is_dir():
                _fs_delete(file)
                file.rmdir()
            else:
                file.unlink()
        # Finally remove root.config
        directory.rmdir()
    # else:
    #     raise FileNotFoundError(f'Directory {directory} does not exist')


def _enable_path_properties(config: dict, root_dir=None) -> dict:
    if not root_dir:
        root_dir = Path.home()

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
                new_config[prop] = root_dir.joinpath(config[prop])
            elif prop == 'config_file':
                new_config[prop] = root_dir.joinpath(config['config_dir'], config[prop])
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
    new_config = dict()
    for prop in config:
        if prop in ['config_dir', 'config_file']:
            new_config[prop] = config[prop].name
        else:
            new_config['config_file'] = config['config_file'].name

    return new_config


class ConfigManager(object):

    @classmethod
    def __init__(cls, config: dict = None, root_dir: Path = None) -> None:

        if not config:
            conf = default_config()
        else:
            conf = config

        if not root_dir:
            # Handle Case where root_dir is String, doesn't matter for Path objects (redundant)
            root_dir = Path.home()
        else:
            root_dir = Path(root_dir)

        """
        If no config provided, default is created and assigned as `cls.config`

        If a Configuration File corresponding to a config  that exists,
        it will take precedence over the provided configuration dict.

        :param config: Application Configuration Directory and File
        :type config: dict
        """
        # Load Existing '.config' IF It Exists
        # Always defers to ON DISK Configuration

        config_file = root_dir.joinpath(conf["config_dir"], conf["config_file"])

        if config_file.exists and config_file.is_file():
            pre_config = loads(config_file.read_text())
            conf = _enable_path_properties(pre_config)
        else:
            conf = _enable_path_properties(conf)

        if not conf["config_dir"].exists():
            root_dir.joinpath(conf["config_dir"]).mkdir(exist_ok=True)

        # Save Configuration File
        disabled = dumps(_disable_path_properties(conf))
        config_file.write_text(disabled)

        cls.config = conf

    @classmethod
    def __del__(cls) -> None:
        _fs_delete(cls.config['config_dir'])

        # Classic Recursive Deletion of a Hierarchy

    def print_config(cls, path=None):
        print(f'{cls.config}')
