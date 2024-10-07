#!/usr/bin/env python3

import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import PosixPath as Path
from random import shuffle

from moduli_assembly import __version__
from moduli_assembly.config_manager.config_manager import ConfigManager


def ISO_UTC_TIMESTAMP() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def default_config():
    '''
    tbd - REMOVE Keylength 2048 BEFORE PRODUCTION
    :return:
    :rtype:
    '''
    return {
        'generator_type': 2,
        'auth_bitsizes': ['2048', '3072', '4096', '6144', '7680', '8192'],
        'config_dir': '.moduli_assembly',
        'config_file': '.config',
        'moduli_dir': '.moduli',
        'moduli_file': 'MODULI_FILE'
    }


def to_be_implemented(function: str):
    print(f'To be Implemented: {function}')


def _fs_delete(dir_path: Path):
    protected_dirs = [
        Path('/'),
        Path('/home'),
        Path('/usr'),
        Path('/usr/local'),
        Path('/var'),
        Path('/opt'),
        Path('/usr/opt'),
        Path('/var/opt')
    ]
    if dir_path in protected_dirs:
        raise PermissionError(f'Illegal Path Selected: {dir_path}')

    if dir_path.exists:
        if dir_path.is_dir():
            for fobject in dir_path.iterdir():
                if fobject.is_dir():
                    _fs_delete(fobject)
                    fobject.rmdir()
                else:
                    fobject.unlink()
        else:
            raise TypeError('Error: supplied path is not a directory')


class ModuliAssembly(ConfigManager):

    @property
    def version(cls) -> str:
        return __version__

    @classmethod
    def __init__(cls, config: dict = None) -> None:
        if config:
            cls.config = config
        else:
            cls.config = default_config()

        for attr in ['config_dir', 'config_file', 'moduli_dir', 'moduli_file', 'generator_type', 'auth_bitsizes']:
            if attr not in cls.config:
                raise AttributeError(f'Config Required Attribute: {attr}: Missing')

        super().__init__(cls.config)
        md = cls.config['config_dir'].joinpath(cls.config['moduli_dir'])
        if not md.parents:  # Root directory name to user's $HOME
            md = Path.home().joinpath(md)

        md.mkdir(exist_ok=True, parents=True)

    @classmethod
    def __del__(cls, app_dir=None):
        '''
        Override ConfigManager's __del__
        :return:
        :rtype:
        '''
        super().__del__(app_dir)

    @classmethod
    def create_checkpoint_filename(cls, path: Path) -> Path:
        return cls.get_moduli_dir().joinpath(f'.{path.name}')

    @classmethod
    def get_moduli_dir(cls) -> Path:
        return cls.config['config_dir'].joinpath(cls.config['moduli_dir'])

    @classmethod
    def create_candidate_path(cls, key_length: int):
        md = cls.get_moduli_dir()  # New Root of Candidate Files
        cpath = md.joinpath(f'{key_length}.candidate_{ISO_UTC_TIMESTAMP()}')
        cpath.touch()
        return cpath

    @classmethod
    def get_screened_path(cls, candidate_path: Path) -> Path:
        return candidate_path.parent.joinpath(str(candidate_path.name)
                                              .replace('candidate', 'screened'))

    @classmethod
    def screen_candidates(cls, candidate_path: Path) -> Path:
        print(f'Screening {candidate_path} for Safe Primes (generator={cls.config['generator_type']})')

        try:
            screen_command = [
                'ssh-keygen',
                '-M', 'screen',
                '-O', f'generator={cls.config['generator_type']}',
                '-O', f'checkpoint={cls.create_checkpoint_filename(candidate_path)}',
                '-f', candidate_path,
                cls.get_screened_path(candidate_path)
            ]
            subprocess.run(screen_command, text=True, check=True)

        except subprocess.CalledProcessError as e:
            print(f'Error screening candidates for {candidate_path.name.split('.')[0]} bit length: {e}')
            exit(1)

        # We've screened the Candidates, Discard File
        candidate_path.unlink()

        return cls.get_screened_path(candidate_path)

    @classmethod
    def generate_candidates(cls, key_length: int, count: int) -> Path:
        print(f'Generating candidate files for modulus size: {key_length}')
        candidate_file = cls.create_candidate_path(key_length)

        for _ in range(count):

            try:
                candidates_temp = tempfile.mktemp()
                # Generate the prime number of the specified bit length
                gen_command = [
                    'ssh-keygen',
                    '-M', 'generate',
                    '-O', f'bits={key_length}',
                    candidates_temp
                ]
                subprocess.run(gen_command, check=True, text=True)

                # Copy Temporary Candidates to Candidates for Screening Run
                with candidate_file.open('a') as cf:
                    with open(candidates_temp, 'r') as ct:
                        cf.write(ct.read())

            except subprocess.CalledProcessError as e:
                raise subprocess.CalledProcessError(f'Error generating {key_length}-bit prime: {e}',
                                                    cmd=gen_command)

        return candidate_file

    @classmethod
    def write_moduli_file(cls, pathname: Path = None) -> Path:
        if not pathname:
            pathname = cls.config['config_dir'].joinpath(cls.config['moduli_file'])

        # Append Time Stamp to File
        ts = ISO_UTC_TIMESTAMP()
        ts_name = '_'.join((str(pathname.absolute()), ts))

        path = Path(ts_name)
        path.touch()
        if pathname.exists():
            pathname.unlink()
        pathname.symlink_to(path, target_is_directory=False)

        # Collect Screened Moduli
        with path.open('w') as mfp:
            mfp.write(f'#/etc/ssh/moduli: moduli_assembly: {ts}\n')
            moduli = [moduli for moduli in
                      cls.get_moduli_dir().glob('????.screened*')]
            moduli.sort()  # Assure We Write Moduli in Increasing Bitsize Order

            for modulus_file in moduli:
                mf_lines = modulus_file.read_text().strip().split('\n')
                shuffle(mf_lines)
                mfp.write('\n'.join(mf_lines))
                mfp.write('\n')  # Repl

        return path

    @classmethod
    def restart_candidate_screening(cls):
        for modulus_file in [moduli for moduli in cls.get_moduli_dir().glob('????.candidate*')]:
            cls.screen_candidates(modulus_file)
            cls.write_moduli_file(modulus_file)

    @classmethod
    def clear_artifacts(cls):
        _fs_delete(cls.get_moduli_dir())

    @classmethod
    def print_config(cls):
        super().print_config(None)
