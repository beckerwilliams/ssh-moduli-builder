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


def _fs_delete(directory: Path = None) -> Path:
    for fobject in directory.iterdir():
        if fobject.is_dir():
            _fs_delete(fobject)
            fobject.rmdir()
        else:
            fobject.unlink()


def fs_delete(directory: Path = None) -> None:
    _fs_delete(directory)
    if directory.is_dir():
        directory.rmdir()


class ConfigManager(object):

    @classmethod
    def __init__(cls, config: dict = None, root_dir: Path = None) -> None:

        if not root_dir:
            root_dir = Path.home()

        if not config:
            config = default_config()

        config['config_dir'] = root_dir.joinpath(config['config_dir'])
        if not config['config_dir'].exists():
            config['config_dir'].mkdir(parents=True, exist_ok=True)

        config_file = config['config_dir'].joinpath(config["config_file"])

        # Read Configuration File, Continue
        if config_file.exists() and config_file.is_file() and config_file.stat().st_size > 0:
            cls.config = _enable_path_properties(loads(config_file.read_text()))
        else:  # Save Current Config
            cls.config = _enable_path_properties(config)
            config_file.write_text(dumps(_disable_path_properties(cls.config)))

    @classmethod
    def print_config(cls):
        print(f'{cls.config}')
