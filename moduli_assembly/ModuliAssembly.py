#!/usr/bin/env python3
__version__ = '0.10.1'

import subprocess
import tempfile
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import PosixPath as Path
from random import shuffle

from moduli_assembly.config_manager.config_manager import ConfigManager


def ISO_UTC_TIMESTAMP() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def default_config():
    """
    tbd - REMOVE Keylength 2048 BEFORE PRODUCTION
    :return:
    :rtype:
    """
    return {
        "generator_type": 2,
        "auth_bitsizes": ["2048", "3072", "4096", "6144", "7680", "8192"],
        "config_dir": ".moduli_assembly",
        "config_file": ".config",
        "moduli_dir": ".moduli",
        "moduli_file": "MODULI_FILE"
    }


def to_be_implemented(function: str):
    print(f'To be Implemented: {function}')


class ModuliAssembly(ConfigManager):

    @classmethod
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
                raise AttributeError(f'Config Required Attribute: {attr}')

        super().__init__(cls.config)
        md = cls.config["config_dir"].joinpath(cls.config["moduli_dir"])
        md.mkdir(exist_ok=True, parents=True)

    @classmethod
    def __del__(cls, app_dir=None):
        """
        Override ConfigManager's __del__
        :return:
        :rtype:
        """
        super().__del__(app_dir)

    @classmethod
    def get_moduli_dir(cls):
        return cls.config['config_dir'].joinpath(cls.config['moduli_dir'])

    @classmethod
    def get_candidate_path(cls, key_length: int):
        md = cls.get_moduli_dir()  # New Root of Candidate Files
        cpath = md.joinpath(f'{key_length}.candidate_{ISO_UTC_TIMESTAMP()}')
        cpath.touch()
        return cpath

    @classmethod
    def get_screened_path(cls, candidate_path: Path):
        return cls.get_moduli_dir().joinpath(candidate_path.name.replace('candidate', 'screened'))

    @classmethod
    def screen_candidates(cls, candidate_path: Path) -> Path:
        print(f'Screening {candidate_path} for Safe Primes (generator={cls.config['generator_type']})')
        checkpoint_file = cls.get_moduli_dir().joinpath(f'.{candidate_path.name}')

        try:
            screen_command = [
                'ssh-keygen',
                '-M', 'screen',
                '-O', f'generator={cls.config['generator_type']}',
                '-O', f'checkpoint={checkpoint_file}',
                '-f', candidate_path,
                cls.get_screened_path(candidate_path)
            ]
            subprocess.run(screen_command, text=True, check=True)

        except subprocess.CalledProcessError as e:
            print(f'Error screening candidates for {candidate_path.name.split(".")[0]} bit length: {e}')
            exit(1)

        # We've screened the Candidates, Discard File
        candidate_path.unlink()
        print(f'{candidate_path} Unlinked')
        return cls.get_screened_path(candidate_path)

    @classmethod
    def generate_candidates(cls, key_length: int, count: int) -> Path:
        print(f'Generating candidate files for modulus size: {key_length}')
        candidate_file = cls.get_candidate_path(key_length)

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
    def write_moduli_file(cls, filename: Path) -> None:
        # Append Time Stamp to File
        ts = ISO_UTC_TIMESTAMP()
        mpath = Path('-'.join((str(filename), ts)))

        # Collect Screened Moduli
        with mpath.open('w') as config_file:
            config_file.write(f'#/etc/ssh/moduli: moduli_assembly: {ts}\n')
            moduli = [moduli for moduli in
                      (cls.config["config_dir"].joinpath(cls.config['moduli_dir'])).glob("????.screened*")]
            moduli.sort()  # Assure We Write Moduli in Increasing Bitsize Order

            for modulus_file in moduli:
                mf_lines = modulus_file.read_text().strip().split('\n')
                shuffle(mf_lines)
                config_file.write('\n'.join(mf_lines))
                config_file.write('\n')  # Repl
        exit(0)

    @classmethod
    def restart_candidate_screening(cls):
        for modulus_file in [moduli for moduli in cls.config["config_dir"].joinpath('.moduli').glob("????.candidate*")]:
            cls.screen_candidates(modulus_file)
            cls.write_moduli_file(modulus_file)

    @classmethod
    def clear_artifacts(cls):
        for file in (cls.config['config_dir'].joinpath(cls.config['moduli_dir'])).glob('*'):
            file.unlink()

    @classmethod
    def print_config(cls):
        super().print_config()


def cl_args():
    parser = ArgumentParser(prog='Moduli Assembly', description='Utility to automate creation of SSH2 Moduli Files')
    parser.add_argument('-b', '--bitsizes',
                        nargs='*',
                        help='space delimited list of requested bitsizes\n\t-b <keylength0> <keylength2> ...', )
    parser.add_argument('-m', '--moduli-dir',
                        default=Path.home().joinpath('.moduli-assembly'),
                        help='Specify location of ./moduli-assembly')
    parser.add_argument('-f', '--config_file',
                        default=Path.home().joinpath(".moduli-assembly/config_file"),
                        help='Select Moduli File Path, default=$HOME/.moduli-assembly')
    # Just Flags, Execute and Exit
    parser.add_argument('-a', '--all',
                        action='store_true',
                        help='Minimally Sufficient and Safe Moduli File. (Run Four in Parallel)!')
    parser.add_argument('-c', '--clear-artifacts',
                        action='store_true',
                        help='Clear Files: generated candidate and screening files.')
    parser.add_argument('-C', '--remove-config-dir',
                        action='store_true',
                        help='Delete Configuration Directory (config_dir)')
    parser.add_argument('-w', '--write_moduli',
                        action='store_true',
                        help='Write Moduli from Current Screened Files and Exit')
    parser.add_argument('-r', '--restart',
                        action='store_true',
                        help='Restart Interrupted Moduli Screening. Ignores `-b <modulus size>`')
    parser.add_argument('-M', '--get-moduli-file',
                        action='store_true',
                        help='Dump Latest Moduli File to STDOUT')
    parser.add_argument('-V', '--version',
                        action='store_true',
                        help='Display moduli-assembly version')
    parser.add_argument('-D', '--moduli-distribution',
                        action='store_true',
                        help='-D, --model-distribution: Print Frequency Distribution of Given Moduli File')
    parser.add_argument('-x', '--export-config',
                        action='store_true',
                        help="Print running configuration")
    return parser


def main() -> None:
    # Process Arguments
    parser = cl_args()
    args = parser.parse_args()

    # Process Configuration File
    cm = ConfigManager(default_config())

    if args.version:
        print(f'{parser.prog}: Version: {__version__}')
        exit(0)

    if args.clear_artifacts:  # Delete and Recreate '.moduli'
        cm.clear_artifacts()
        exit(0)

    if args.remove_config_dir:
        del cm
        exit(0)

        # Dump Latest config_file to STDOUT
    if args.export_config:
        cm.print_config()
        exit(0)

    # We always write the MODULI file when done - Here we ONLY Write Current based on MODULI/*.screened*
    if args.write_moduli:
        cm.write_moduli_file(cm.config["config_file"])
        print(f'Wrote moduli file, {cm.config["config_file"]}, and exiting.')
        exit(0)

    if args.restart:
        print(f'Restarted candidate screening')
        cm.restart_candidate_screening()
        cm.write_moduli_file('MODULI_FILE')
        exit(0)

    # -a, --all trumps any provided key_length parameters
    if args.all:
        bitsizes = list(cm.config["AUTH_KEY_LENGTHS"])
    elif args.bitsizes:
        bitsizes = args.bitsizes
    else:
        print(f'ERROR: No bitsizes, You must Select One Argument Type moduli_assembly.py [-a, -b, -r, -w]')
        exit(1)

    bitsizes.sort()  # We'll run in Increasing Order. The opposite (.reverse()) will take the LONGEST runs, first

    run_bits = {}
    for key_length in bitsizes:

        if key_length not in cm.config["AUTH_KEY_LENGTHS"]:
            print(f'Bitsize: {key_length} is not Enabled')
            print('Enabled Bitsizes: "[-b 2048 3072 4096 6144 7680 8192]"')
            exit(1)

        run_bits[key_length] = bitsizes.count(key_length)

    candidates = [cm.generate_candidates(int(key_length), run_bits[key_length])
                  for key_length in run_bits if run_bits[key_length]]

    # Screen Candidates, Log Screened File Paths
    with cm.config["config_dir"].joinpath('screened-files.txt').open('a') as cf:
        [cf.write(f'Screened File: {cm.get_screened_path(candidate)}\n') for candidate in candidates]
        [cm.screen_candidates(candidate) for candidate in candidates]

    # Create /etc/ssh/moduli file
    cm.write_moduli_file('MODULI_FILE')


if __name__ == '__main__':
    main()
