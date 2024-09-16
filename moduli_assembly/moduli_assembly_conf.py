#!/usr/bin/env python
from json import (dumps, loads)
from pathlib import PosixPath as Path


# TBD Configuration Editor


def default_conf() -> dict:  # Default moduli-assembly Configuration

    return {
        "GENERATOR_TYPE": 2,
        "AUTH_BITSIZES": ["2048", "3072", "4096", "6144", "7680", "8192"],
        "MODULI_DIR": str(Path.home().joinpath(".moduli-assembly")),
        "MODULI_FILE": str(Path.home().joinpath(".moduli-assembly/MODULI_FILE"))
    }


def pre_save_conf_filter(conf: dict) -> dict:
    # Converts PATH Objects in Python Dict to Strings
    new_conf = {}
    for prop in conf:
        if prop == 'MODULI_DIR' or prop == 'MODULI_FILE':
            new_conf[prop] = str(conf[prop])
        else:
            new_conf[prop] = conf[prop]
    return new_conf


def post_load_conf_filter(conf: dict) -> dict:
    # Converts File Path STRING Objects to Python Path (pathlib) Objects
    new_conf = {}
    for prop in conf:
        if prop == 'MODULI_DIR' or prop == 'MODULI_FILE':
            new_conf[prop] = Path(conf[prop])
        else:
            new_conf[prop] = conf[prop]
    return new_conf


def save_conf(**kwargs: dict) -> dict:
    # Identify Module Directory
    if 'MODULI_DIR' in kwargs.keys():
        moduli_directory = kwargs['moduli_dir']
    else:
        moduli_directory = Path.home().joinpath('.moduli-assembly')

    # Identify configuration (and Convert Python 'Path' objects to 'str': pre_save_conf_filter
    if 'conf' in kwargs.keys():
        conf = pre_save_conf_filter(kwargs['conf'])
    else:
        conf = pre_save_conf_filter(default_conf())

    moduli_directory.joinpath('config.json').write_text(dumps(conf))

    return conf


def load_conf(**kwargs: dict) -> dict:
    # Identify Module Directory
    if 'moduli_dir' in kwargs.keys():
        moduli_dir = kwargs['moduli_dir']

    else:  # Default Directory
        moduli_dir = Path.home().joinpath('.moduli-assembly')

    # Verify Moduli Directory Exists (and contains subdirectory `.moduli`)
    if not moduli_dir.exists():
        moduli_dir.joinpath('.moduli').mkdir(parents=True, exist_ok=True)

    # Verify Existing and Non-Empty config.json file
    if not moduli_dir.joinpath('config.json').exists() or moduli_dir.joinpath('config.json').stat().st_size < 3:
        return post_load_conf_filter(save_conf(conf=default_conf()))
    else:
        return post_load_conf_filter(loads(moduli_dir.joinpath('config.json').read_text()))
