#!/usr/bin/env python
from json import (dump, load)
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
    for prop in conf:
        if prop == 'MODULI_DIR' or prop == 'MODULI_FILE':
            conf[prop] = str(conf[prop])
    return conf


def post_load_conf_filter(conf: dict) -> dict:
    # Converts File Path STRING Objects to Python Path (pathlib) Objects
    for prop in conf:
        if prop == 'MODULI_DIR' or prop == 'MODULI_FILE':
            conf[prop] = Path(conf[prop])
    return conf


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

    with moduli_directory.joinpath('config.json').open(mode='w') as conf_wfp:
        dump(conf, conf_wfp, indent=4)

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
    if not moduli_dir.joinpath('config.json').exists() or moduli_dir.joinpath('config.json').stat().st_size == 0:
        # We've no Config - Obtain Default, Save  and Use It
        return post_load_conf_filter(save_conf(conf=default_conf()))
    else:
        # We have a conf, lets use it
        with moduli_dir.joinpath('config.json').open('r') as conf_rfp:
            return post_load_conf_filter(load(conf_rfp))
