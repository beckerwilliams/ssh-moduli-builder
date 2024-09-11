#!/usr/bin/env python

import subprocess
import tempfile
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import PosixPath as Path
from random import shuffle

# Constants
GENERATOR_TYPE = 2
AUTH_BITSIZES = ('2048', '3072', '4096', '6144', '7680', '8192')
MODULI_DIR = Path('MODULI')  # Location of MODULI Directory
MODULI_FILE = Path("MODULI_PROTO")


def create_moduli_dir() -> None:
    if not MODULI_DIR.exists():
        MODULI_DIR.mkdir(parents=True, exist_ok=True)


def ISO_UTC_TIMESTAMP() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def cl_args():
    parser = ArgumentParser(description='Moduli Assembly')
    parser.add_argument('-a', '--all',
                        action='store_true', help='Minimally Sufficient and Safe Moduli File. (Run Four in Parallel)!')
    parser.add_argument('-w', '--write_moduli',
                        action='store_true', help='Write Moduli from Current Screened')
    parser.add_argument('-r', '--restart',
                        action='store_true', help='Restart Interrupted Moduli Screening')
    parser.add_argument('-b', '--bitsizes',
                        nargs='*', help='space delimited list of requested bitsizes', required=False)
    return parser.parse_args()


def get_candidate_path(bitsize: int) -> Path:
    p = Path(f'{MODULI_DIR}/{bitsize}.candidate_{ISO_UTC_TIMESTAMP()}')
    p.touch()  # Assure Empty File Exists
    return p


def get_screened_path(candidate_path: Path) -> Path:
    return MODULI_DIR.joinpath(Path(candidate_path.name.replace('candidate', 'screened')))


def screen_candidates(candidate_path: Path) -> None:
    print(f'Screening {candidate_path} for Safe Primes (generator={GENERATOR_TYPE})')
    cp_file = MODULI_DIR.joinpath(f'.{candidate_path.name}')

    try:
        screen_command = [
            'ssh-keygen',
            '-M', 'screen',
            '-O', f'generator={GENERATOR_TYPE}',
            '-O', f'checkpoint={cp_file}',
            '-f', candidate_path,
            get_screened_path(candidate_path)
        ]
        subprocess.run(screen_command, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f'Error screening candidates for {candidate_path.name.split(".")[0]} bit length: {e}')

    # We've screened the Candidates, Discard File
    candidate_path.unlink()


def generate_candidates(key_length: int, count: int) -> Path:
    print(f'Generating candidate files for keylength: {key_length}')
    candidate_file = get_candidate_path(key_length)

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

    return candidate_file


def write_moduli_file(mpath: Path) -> None:
    # print(f'Compiling MODULI File: {mpath.name}')

    # Collect Screened Moduli
    with mpath.open('w') as moduli_file:
        moduli_file.write(f'#/etc/ssh/moduli: DCRUNCH {ISO_UTC_TIMESTAMP()}\n')
        moduli = [moduli for moduli in MODULI_DIR.glob("????.screened*")]
        moduli.sort()  # Assure We Write Moduli in Increasing Bitsize Order
        for modulus_file in moduli:
            # Shuffle Order of Screened Moduli Prior to Inclusion in Final MODULI File
            randomize_file_record_order(modulus_file)
            # Write the moduli
            with Path(modulus_file).open('r') as mf:
                moduli_file.write(mf.read())
                moduli_file.write('\n')  # Screened Files LACK Trailing NEWLINE


def restart_candidate_screening() -> None:
    for modulus_file in [moduli for moduli in MODULI_DIR.glob("????.candidate*")]:
        screen_candidates(modulus_file)


def randomize_file_record_order(screened_fn: Path) -> None:
    # print(f'Randomizing Bitsize Moduli File: {screened_fn}')
    with screened_fn.open('r') as cf:
        lines = cf.read().strip().split('\n')
        shuffle(lines)
    # Re-Write Screened File Entries with Randomized Order
    with screened_fn.open('w') as cf:
        cf.write('\n'.join(lines))


def main() -> None:
    args = cl_args()
    print(f'args: {args}')

    # We always write the MODULI file when done - Here we ONLY Write Current based on MODULI/*.screened*
    if args.write_moduli:
        write_moduli_file(MODULI_FILE)
        print(f'Wrote moduli file, {MODULI_FILE}, and exiting.')
        exit(0)

    if args.restart:
        print(f'Restarted candidate screening')
        restart_candidate_screening()
        exit(0)

    # -a, --all trumps any provided bitsize parameters
    bitsizes = None
    if args.all:
        bitsizes = list(AUTH_BITSIZES)
    elif args.bitsizes:
        bitsizes = args.bitsizes
    else:
        print(f'ERROR: No bitsizes, You must Select One Argument Type moduli_assembly.py [-a, -b, -r, -w]')
        exit(1)

    bitsizes.sort()  # We'll run in Increasing Order. The opposite (.reverse()) will take the LONGEST runs, first

    # Create MODULI Working Directory
    create_moduli_dir()

    # Validate that requested Bitsizes are in the list of acceptable values
    # and Apply Counts of Moduli found in Args
    run_bits = {}
    for bitsize in bitsizes:

        if bitsize not in AUTH_BITSIZES:
            print(f'Bitsize: {bitsize} is not Enabled')
            print('Enabled Bitsizes: "[-b [2048] [3072] [4096] [6144] [7680] [8192]]"')
            exit(1)

        run_bits[bitsize] = bitsizes.count(bitsize)

    candidates = [generate_candidates(int(bitsize), int(run_bits[bitsize]))
                  for bitsize in run_bits if run_bits[bitsize]]

    # Screen Candidates, Log Screened File Paths
    with MODULI_DIR.joinpath('screened-files.txt').open('a') as cf:
        for candidate in candidates:
            cf.write(f'Screened File: {get_screened_path(candidate)}\n')
            screen_candidates(candidate)

    # Create PROTO /etc/ssh/moduli File
    write_moduli_file(MODULI_FILE)


if __name__ == '__main__':
    main()
