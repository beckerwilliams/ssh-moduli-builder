#!/usr/bin/env python

from json import dumps, loads
from pathlib import PosixPath as Path


def file_is_empty(file: Path):
    if not file.exists():
        raise Exception(f'File {file} does not exist')
    res = file.stat(follow_symlinks=True).st_size


def default_conf() -> dict:
    return {
        "GENERATOR_TYPE": 2,
        "AUTH_BITSIZES": ('2048', '3072', '4096', '6144', '7680', '8192'),
        "MODULI_DIR": '.moduli-assembly',
        "MODULI_FILE": '.moduli-assembly/MODULI_FILE'
    }


def save_conf(conf: dict) -> dict:
    if not conf:  # Save DEFAULT Config
        MODULI_DIR = Path.home().joinpath('.moduli-assembly')
        config = MODULI_DIR.joinpath('config.json')
        conf = default_conf()
        config.write_text(dumps(conf, indent=4))

        return conf
    else:
        conf_build = {}
        for prop in conf:
            if str(prop) == 'MODULI_DIR' or str(prop) == 'MODULI_FILE':
                conf_build[prop] = str(conf[prop])
            else:
                conf_build[prop] = conf[prop]

        return conf_build


def load_conf(moduli_directory=str(Path.home().joinpath('.moduli-assembly'))):
    config = Path(moduli_directory).joinpath("config.json")
    conf = loads(config.read_text())
    for prop in conf:
        if str(prop) == 'MODULI_DIR' or str(prop) == 'MODULI_FILE':
            conf[prop] = Path(conf[prop])
    return conf


def moduli_conf(
        moduli_directory: str = str(Path.home().joinpath(".moduli-assembly")),
        moduli_file: str = "MODULI_FILE"
) -> dict:
    config = Path(moduli_directory).joinpath("config.json")
    if config.exists() and file_is_empty(config):
        return load_conf(config)

    else:  # Create & Save Default in Current Moduli Directory
        conf = {
            "GENERATOR_TYPE": 2,
            "AUTH_BITSIZES": ('2048', '3072', '4096', '6144', '7680', '8192'),
            "MODULI_DIR": Path(f'{moduli_directory}'),
            "MODULI_FILE": Path(f'{moduli_directory}').joinpath(moduli_file)
        }
        save_conf(conf)
        return conf


if __name__ == "__main__":
    print(save_conf(None))
    # exit()
    conf = load_conf(Path.home().joinpath(".moduli-assembly"))
    print(conf)

#     else:  # Create and Save DEFAULT Config, AND Return DEFAULT Config
#         if "MODULI_DIRECTORY" in conf:
#             conf["MODULI_DIRECTORY"] = Path(conf["MODULI_DIRECTORY"])
#         if "MODULI_FILE" in conf:
#             conf["MODULI_FILE"] = Path(conf["MODULI_FILE"])
#         return conf
