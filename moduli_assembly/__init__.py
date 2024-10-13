#!/usr/bin/env python3

import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import PosixPath as Path
from random import shuffle

from config_manager import ConfigManager

__version__ = '0.10.3'


def ISO_UTC_TIMESTAMP() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def default_config():
    """
    tbd - REMOVE Keylength 2048 BEFORE PRODUCTION
    :return:
    :rtype:
    """
    return {
        'generator_type': 2,
        'auth_bitsizes': ['2048', '3072', '4096', '6144', '7680', '8192'],
        'config_dir': '.moduli_assembly',
        'config_file': '.config',
        'moduli_dir': '.moduli',
        'moduli_file': 'MODULI_FILE'
    }


_config_required_attrs = default_config().keys()


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
    def version(self) -> str:
        return __version__

    @classmethod
    def __init__(self, config: dict = None, root_dir: Path = None) -> None:

        if not root_dir:
            root_dir = Path.home()

        if not config:
            config = default_config()

        for attr in _config_required_attrs:
            if attr not in config:
                raise AttributeError(f'Config Required Attribute: {attr}: Missing')

        super().__init__(config, root_dir)

        # Operational Config has 'moduli_dir' as full path under selected config dir
        self.config['moduli_dir'] = self.config['config_dir'].joinpath(self.config['moduli_dir'])
        self.config['moduli_dir'].mkdir(exist_ok=True)

    # @classmethod
    # def __del__(self):
    #     """
    #     Override ConfigManager's __del__
    #     :return: None
    #     :rtype:
    #     :raises: FileNotFoundError
    #     :raises: FileExistsError
    #     """
    #     super().__del__()

    @classmethod
    def create_checkpoint_filename(self, path: Path) -> Path:
        return self.config['moduli_dir'].joinpath(f'.{path.name}')

    @classmethod
    def create_candidate_path(self, key_length: int):
        candidate_path = self.config['moduli_dir'].joinpath(f'{key_length}.candidate_{ISO_UTC_TIMESTAMP()}')
        candidate_path.touch()
        return candidate_path

    @classmethod
    def get_screened_path(self, candidate_path: Path) -> Path:
        return candidate_path.parent.joinpath(str(candidate_path.name)
                                              .replace('candidate', 'screened'))

    @classmethod
    def screen_candidates(self, candidate_path: Path) -> Path:
        print(f'Screening {candidate_path} for Safe Primes (generator={self.config['generator_type']})')

        try:
            screen_command = [
                'ssh-keygen',
                '-M', 'screen',
                '-O', f'generator={self.config['generator_type']}',
                '-O', f'checkpoint={self.create_checkpoint_filename(candidate_path)}',
                '-f', candidate_path,
                self.get_screened_path(candidate_path)
            ]
            subprocess.run(screen_command, text=True, check=True)

        except subprocess.CalledProcessError as e:
            print(f'Error screening candidates for {candidate_path.name.split('.')[0]} bit length: {e}')
            exit(1)

        # We've screened the Candidates, Discard File
        candidate_path.unlink()

        return self.get_screened_path(candidate_path)

    @classmethod
    def generate_candidates(self, key_length: int, count: int) -> Path:
        print(f'Generating candidate files for modulus size: {key_length}')
        candidate_file = self.create_candidate_path(key_length)

        for _ in range(count):
            gen_command = []

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
    def write_moduli_file(self, pathname: Path = None) -> Path:
        if not pathname:
            pathname = Path(self.config['config_dir']).joinpath(self.config['moduli_file'])
        else:
            pathname = Path(pathname)  # a Hack

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
                      self.config['moduli_dir'].glob('????.screened*')]
            moduli.sort()  # Assure We Write Moduli in Increasing Bitsize Order

            for modulus_file in moduli:
                mf_lines = modulus_file.read_text().strip().split('\n')
                shuffle(mf_lines)
                mfp.write('\n'.join(mf_lines))
                mfp.write('\n')  # Repl

        return path

    @classmethod
    def restart_candidate_screening(self):
        for modulus_file in [moduli for moduli in self.config['moduli_dir'].glob('????.candidate*')]:
            self.screen_candidates(modulus_file)
            self.write_moduli_file(modulus_file)

    @classmethod
    def clear_artifacts(self):
        _fs_delete(self.config['moduli_dir'])

    @classmethod
    def print_config(self, path: Path = None):
        super().print_config()
