#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import PosixPath as Path

from moduli_assembly.ModuliAssembly import (ModuliAssembly)


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
    cm = ModuliAssembly()

    if args.version:
        print(f'{parser.prog}: Version: {cm.version}')
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
        cm.write_moduli_file(cm.config['moduli_file'])
        print(f'Wrote moduli file, {cm.config['moduli_file']}, and exiting.')
        exit(0)

    if args.restart:
        print(f'Restarted candidate screening')
        cm.restart_candidate_screening()
        cm.write_moduli_file('MODULI_FILE')
        exit(0)

    # -a, --all trumps any provided key_length parameters
    if args.all:
        bitsizes = list(cm.config["auth_key_lengths"])
    elif args.bitsizes:
        bitsizes = args.bitsizes
    else:
        print(f'ERROR: No bitsizes, You must Select One Argument Type moduli_assembly.py [-a, -b, -r, -w]')
        exit(1)

    bitsizes.sort()  # We'll run in Increasing Order. The opposite (.reverse()) will take the LONGEST runs, first

    run_bits = {}
    for key_length in bitsizes:

        if key_length not in cm.config["auth_bitsizes"]:
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
