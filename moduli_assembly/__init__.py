import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import PosixPath as Path
from random import shuffle

from config_manager import (ConfigManager)

__version__ = '1.0.7'  # Dependent on pyproject.toml VERSION Manual Sync


def ISO_UTC_TIMESTAMP() -> str:
    """

    :return: Current ISO TimeStamp, TZ=UTC
    :rtype: str
    """
    return datetime.now(tz=timezone.utc).isoformat()


def default_config() -> dict:
    """

    :return: Sufficient configuration for Moduli_Assembly Operation
    :rtype: dict
    """
    return {
        'generator_type': 2,
        'auth_bitsizes': [3072, 4096, 6144, 7680, 8192],
        'config_dir': '.moduli_assembly',
        'config_file': '.config',
        'moduli_dir': '.moduli',
        'moduli_file': 'MODULI_FILE'
    }


class ModuliAssembly(ConfigManager):

    @property
    def version(self) -> str:
        """

        :return: version
        :rtype: str
        """

        return __version__

    @classmethod
    def __init__(self, config: dict = None, root_dir: Path = None) -> None:
        """

        :param config: Moduli Assembly Config
        :type config: dict
        :param root_dir: moduli_assembly configuration's root directory
        :type root_dir: PosixPath
        """
        if not root_dir:
            root_dir = Path.home()

        if not config:
            config = default_config()

        # Validate Attributes
        for attr in default_config().keys():
            if attr not in config:
                raise AttributeError(f'Config Required Attribute: {attr}: Missing')

        super().__init__(config, root_dir)

        # Operational Config has 'moduli_dir' as full path under selected config dir
        self.config['moduli_dir'] = config['config_dir'].joinpath(config['moduli_dir'])
        self.config['moduli_dir'].mkdir(exist_ok=True)
        self.config['moduli_file'] = config['config_dir'].joinpath(config['moduli_file'])
        self.config['auth_bitsizes'] = config['auth_bitsizes']
        self.config['generator_type'] = config['generator_type']

    @classmethod
    def create_checkpoint_filename(self, path: Path) -> Path:
        """

        :param path: name of checkpoint file
        :type path: PosixPath
        :return: Name of Checkpoint File
        :rtype: PosixPath
        """
        return self.config['moduli_dir'].joinpath(f'.{path.name}')

    @classmethod
    def create_candidate_path(self, key_length: int):
        """

        :param key_length: Max Bitlength of Moduli to Process
        :type key_length: int
        :return: Candidate Path
        :rtype: PosixPath
        """
        candidate_path = self.config['moduli_dir'].joinpath(f'{key_length}.candidate_{ISO_UTC_TIMESTAMP()}')
        candidate_path.touch()
        return candidate_path

    @classmethod
    def get_screened_path(self, candidate_path: Path) -> Path:
        """

        :param candidate_path: Location of Generated Moduli to Screen
        :type candidate_path: PosixPath
        :return: Path of Screened Moduli file
        :rtype: PosixPath
        """
        return candidate_path.parent.joinpath(str(candidate_path.name)
                                              .replace('candidate', 'screened'))

    @classmethod
    def screen_candidates(self, candidate_path: Path) -> Path:
        """

        :param candidate_path: Location of Generated Moduli to Screen
        :type candidate_path: PosixPath
        :return: Candidate Path
        :rtype: PosixPath
        """
        print(f'Screening {candidate_path} for Safe Primes (generator={self.config["generator_type"]})')

        try:
            screen_command = [
                'ssh-keygen',
                '-M', 'screen',
                '-O', f'generator={self.config["generator_type"]}',
                '-O', f'checkpoint={self.create_checkpoint_filename(candidate_path)}',
                '-f', candidate_path,
                self.get_screened_path(candidate_path)
            ]
            subprocess.run(screen_command, text=True, check=True)

        except subprocess.CalledProcessError as e:
            print(f'Error screening candidates for {candidate_path.name.split(".")[0]} bit length: {e}')
            exit(1)

        # We've screened the Candidates, Discard File
        if candidate_path.exists():  # Address Issue 1, unlink of non-existant file **Fixed?***
            candidate_path.unlink()

        return self.get_screened_path(candidate_path)

    @classmethod
    def generate_candidates(self, key_length: int, count: int) -> Path:
        """

        :param key_length: Max Moduli Key Length
        :type key_length: int
        :param count: Number of Moduli with same Key Length to process
        :type count: int
        :return: Candidate File Path
        :rtype: PosixPath
        """
        print(f'Generating candidate files for modulus size: {key_length}')
        candidate_file = self.create_candidate_path(key_length)

        for _ in range(count):
            gen_command = []

            try:
                _, candidates_temp = tempfile.mkstemp()  # Switching
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

                Path(candidates_temp).unlink()

            except subprocess.CalledProcessError as e:
                raise subprocess.CalledProcessError(f'Error generating {key_length}-bit prime: {e}',
                                                    cmd=gen_command)

        return candidate_file

    @classmethod
    def create_moduli_file(self, f_path: Path = None) -> Path:
        """

        :param f_path:
        :type f_path:
        :return:
        :rtype:
        """

        if not f_path:
            f_path = self.config['config_dir'].joinpath(self.config['moduli_file'])

        # Append Time Stamp to File
        ts = ISO_UTC_TIMESTAMP()
        ts_name = '_'.join((str(f_path.absolute()), ts))

        path = Path(ts_name)
        path.touch()

        # if pathname.exists():
        if f_path.exists():
            f_path.unlink(missing_ok=True)

        f_path.symlink_to(path, target_is_directory=False)

        # Collect Screened Moduli
        with path.open('w') as mfp:
            # Here we collect all screened moduli files in .moduli_assembly/.moduli
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
        """
        Restart Screening of Any Interrupted Screening of Candidate Modulus Files

        """
        for modulus_file in [moduli for moduli in self.config['moduli_dir'].glob('????.candidate*')]:
            self.screen_candidates(modulus_file)

    @classmethod
    def clear_artifacts(self) -> None:
        """

        :return:
        :rtype:
        """
        for file in self.config['moduli_dir'].glob('*'):
            file.unlink()
