#!/usr/bin/env python3
__version__ = '0.9.6'

import subprocess
import tempfile
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import PosixPath as Path
from random import shuffle

from moduli_assembly.moduli_assembly_conf import load_conf



def ISO_UTC_TIMESTAMP() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def create_moduli_dir(conf) -> Path:
    if 'moduli_dir' not in conf:
        moduli_dir = Path.home().joinpath('.moduli-assembly/.moduli')
    else:
        moduli_dir = conf['MODULI_DIR'].joinpath('.moduli')

    # Include Moduli Candidates Sub-Directory in `mkdir`
    moduli_dir.joinpath('.moduli').mkdir(parents=True, exist_ok=True)

    return moduli_dir


def cl_args():
    parser = ArgumentParser(prog='Moduli Assembly', description='Utility to automate creation of SSH2 Moduli Files')
    parser.add_argument('-b', '--bitsizes',
                        nargs='*',
                        help='space delimited list of requested bitsizes\n-b <keylength0> <keylength2> ...', )
    parser.add_argument('-m', '--moduli-dir',
                        default=Path.home().joinpath('.moduli-assembly'),
                        help='Specify location of ./moduli-assembly')
    parser.add_argument('-f', '--moduli_file',
                        default=Path.home().joinpath(".moduli-assembly/MODULI_FILE"),
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
                        help='Delete Configuration Directory (MODULI_DIR)')
    parser.add_argument('-w', '--write_moduli',
                        action='store_true',
                        help='Write Moduli from Current Screened Files and Exit')
    parser.add_argument('-r', '--restart',
                        action='store_true',
                        help='Restart Interrupted Moduli Screening. Ignores `-b <modulus size>`')
    parser.add_argument('-M', '--get-moduli-file',
                        action='store_true',
                        help='Dump Latest Moduli FIle to STDOUT')
    parser.add_argument('-V', '--version',
                        action='store_true',
                        help='Display moduli-assembly version')
    return parser


def version() -> str:
    return __version__


def get_candidate_path(bitsize: int, conf: dict) -> Path:
    p = conf["MODULI_DIR"].joinpath('.moduli')  # New Root of Candidate Files
    p = p.joinpath(f'{bitsize}.candidate_{ISO_UTC_TIMESTAMP()}')
    p.touch()  # Assure Empty File Exists
    return p


def get_screened_path(candidate_path: Path, conf: dict) -> Path:
    return (conf["MODULI_DIR"].joinpath('.moduli')
            .joinpath(Path(candidate_path.name.replace('candidate', 'screened'))))


def screen_candidates(candidate_path: Path, conf: dict) -> None:
    print(f'Screening {candidate_path} for Safe Primes (generator={conf["GENERATOR_TYPE"]})')
    checkpoint_file = conf["MODULI_DIR"].joinpath('.moduli').joinpath(f'.{candidate_path.name}')

    try:
        screen_command = [
            'ssh-keygen',
            '-M', 'screen',
            '-O', f'generator={conf["GENERATOR_TYPE"]}',
            '-O', f'checkpoint={checkpoint_file}',
            '-f', candidate_path,
            get_screened_path(candidate_path, conf)
        ]
        subprocess.run(screen_command, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f'Error screening candidates for {candidate_path.name.split(".")[0]} bit length: {e}')
        exit(1)

    # We've screened the Candidates, Discard File
    candidate_path.unlink()
    print(f'{candidate_path} Unlinked')


def generate_candidates(key_length: int, count: int, conf: dict) -> Path:
    print(f'Generating candidate files for modulus size: {key_length}')
    candidate_file = get_candidate_path(key_length, conf)

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
            print(f'Error generating {key_length}-bit prime: {e}')
            exit(1)

    return candidate_file


def write_moduli_file(path: Path, conf: dict) -> None:
    # Append Time Stamp to File
    ts = ISO_UTC_TIMESTAMP()
    mpath = Path('-'.join((str(path), ts)))

    # Save a Softlink to the Latest moduli file, simply named MODULI_FILE
    if path.is_symlink():
        path.unlink()
        path.symlink_to(mpath)
    else:
        path.symlink_to(mpath)

    print(f'Compiling MODULI File: {path.name} -> {mpath.name}')

    # Collect Screened Moduli
    with mpath.open('w') as moduli_file:
        moduli_file.write(f'#/etc/ssh/moduli: MODULI-ASSEMBLY: {ts}\n')
        moduli = [moduli for moduli in conf["MODULI_DIR"].joinpath('.moduli').glob("????.screened*")]
        moduli.sort()  # Assure We Write Moduli in Increasing Bitsize Order

        for modulus_file in moduli:
            mf_lines = modulus_file.read_text().strip().split('\n')
            shuffle(mf_lines)
            moduli_file.write('\n'.join(mf_lines))
            moduli_file.write('\n')  # Replace Termiating `newline` stripped on read


def restart_candidate_screening(conf) -> None:
    for modulus_file in [moduli for moduli in conf["MODULI_DIR"].joinpath('.moduli').glob("????.candidate*")]:
        screen_candidates(modulus_file, conf)
    write_moduli_file(modulus_file, conf)
    exit(0)


def clear_artifacts(conf: dict) -> None:
    for file in conf['MODULI_DIR'].joinpath('.moduli').glob('*'):
        file.unlink()
        exit(0)


def rm_config_dir(conf: dict) -> None:
    for file in conf['MODULI_DIR'].joinpath('.moduli').glob('*'):
        file.unlink()
    conf['MODULI_DIR'].joinpath('.moduli').rmdir()
    for file in conf['MODULI_DIR'].glob('*'):
        file.unlink()
    conf['MODULI_DIR'].rmdir()
    exit(0)


def main() -> None:
    parser = cl_args()

    args = cl_args().parse_args()

    conf = load_conf(moduli_dir=args.moduli_dir)  # Load Saved (default) Configuration

    if args.version:
        print(f'{parser.prog}: Version: {version()}')
        exit(0)

    if args.clear_artifacts:  # Delete and Recreate '.moduli'
        clear_artifacts(conf)
        exit(0)

    if args.remove_config_dir:
        rm_config_dir(conf)
        exit(0)

    # Dump Latest MODULI_FILE to STDOUT
    if args.get_moduli_file:
        if not conf["MODULI_FILE"].exists():
            write_moduli_file(conf["MODULI_FILE"], conf)
            if not conf["MODULI_FILE"].exists():
                print("Please Generate a New MODULI Files, None Exist")
                exit(1)
        print(conf['MODULI_FILE'].read_text())
        exit(0)

    # We always write the MODULI file when done - Here we ONLY Write Current based on MODULI/*.screened*
    if args.write_moduli:
        write_moduli_file(conf["MODULI_FILE"], conf)
        print(f'Wrote moduli file, {conf["MODULI_FILE"]}, and exiting.')
        exit(0)

    if args.restart:
        print(f'Restarted candidate screening')
        restart_candidate_screening(conf)
        write_moduli_file(conf["MODULI_FILE"], conf)
        exit(0)

    # -a, --all trumps any provided bitsize parameters
    if args.all:
        bitsizes = list(conf["AUTH_BITSIZES"])
    elif args.bitsizes:
        bitsizes = args.bitsizes
    else:
        print(f'ERROR: No bitsizes, You must Select One Argument Type moduli_assembly.py [-a, -b, -r, -w]')
        exit(1)

    bitsizes.sort()  # We'll run in Increasing Order. The opposite (.reverse()) will take the LONGEST runs, first

    run_bits = {}
    for bitsize in bitsizes:

        if bitsize not in conf["AUTH_BITSIZES"]:
            print(f'Bitsize: {bitsize} is not Enabled')
            print('Enabled Bitsizes: "[-b 2048 3072 4096 6144 7680 8192]"')
            exit(1)

        run_bits[bitsize] = bitsizes.count(bitsize)

    candidates = [generate_candidates(int(bitsize), run_bits[bitsize], conf)
                  for bitsize in run_bits if run_bits[bitsize]]

    # Screen Candidates, Log Screened File Paths
    with conf["MODULI_DIR"].joinpath('screened-files.txt').open('a') as cf:
        [cf.write(f'Screened File: {get_screened_path(candidate, conf)}\n') for candidate in candidates]
        [screen_candidates(candidate, conf) for candidate in candidates]

    # Create /etc/ssh/moduli file
    write_moduli_file(conf["MODULI_FILE"], conf)


if __name__ == '__main__':
    main()
