#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import Dict, List, Optional

from moduli_assembly import ModuliAssembly  # Assuming this is correct, adjust if necessary
from moduli_assembly.scripts.moduli_infile import main as moduli_infile


def cl_args() -> argparse.ArgumentParser:
    """
    Set up command-line arguments for the Moduli Assembly utility.

    :return: Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(prog='Moduli Assembly',
                                     description='Utility to automate creation of SSH2 Moduli Files')
    parser.add_argument('-b', '--bitsizes', nargs='*', type=int, help='Space-delimited list of requested bitsizes')
    parser.add_argument('-m', '--moduli-dir', default=Path.home() / '.moduli-assembly', type=Path,
                        help='Specify location of .moduli-assembly directory')
    parser.add_argument('-f', '--config-file', default=Path.home() / '.moduli-assembly' / 'config_file', type=Path,
                        help='Select Moduli File Path, default=$HOME/.moduli-assembly/config_file')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Generate minimally sufficient and safe moduli file (run four in parallel).')
    parser.add_argument('-c', '--clear-artifacts', action='store_true',
                        help='Clear generated candidate and screening files.')
    parser.add_argument('-C', '--remove-config-dir', action='store_true', help='Delete configuration directory.')
    parser.add_argument('-w', '--write-moduli', action='store_true',
                        help='Write moduli from current screened files and exit.')
    parser.add_argument('-r', '--restart', action='store_true',
                        help='Restart interrupted moduli screening. Ignores `-b `.')
    parser.add_argument('-M', '--get-moduli-file', action='store_true', help='Dump latest moduli file to STDOUT.')
    parser.add_argument('-V', '--version', action='store_true', help='Display moduli-assembly version.')
    parser.add_argument('-D', '--moduli-distribution', action='store_true',
                        help='Print frequency distribution of the given moduli file.')
    parser.add_argument('-x', '--export-config', action='store_true', help="Print running configuration.")
    return parser


def main() -> None:
    """
    Main entry point for all Moduli Assembly operations.
    """
    parser = cl_args()
    args = parser.parse_args()

    cm = ModuliAssembly()

    if args.version:
        print(f'{parser.prog}: Version: {cm.version}')
        return

    if args.clear_artifacts:
        try:
            cm.clear_artifacts()
        except Exception as e:
            print(f"Error clearing artifacts: {e}")
        return

    if args.remove_config_dir:
        try:
            del cm
        except Exception as e:
            print(f"Error removing config directory: {e}")
        return

    if args.export_config:
        cm.print_config()
        return

    if args.write_moduli:
        try:
            cm.create_moduli_file(cm.config['moduli_file'])
            print(f'Wrote moduli file to {cm.config["moduli_file"]} and exiting.')
        except Exception as e:
            print(f"Error writing moduli file: {e}")
        return

    if args.moduli_distribution:
        moduli_infile()
        # cm.print_moduli_distribution()
        return

    if args.restart:
        print('Restarting candidate screening')
        cm.restart_candidate_screening()
        cm.create_moduli_file()
        return

    bitsizes = args.bitsizes if args.bitsizes else list(cm.config['auth_bitsizes']) if args.all else None
    if not bitsizes:
        print('ERROR: No bitsizes specified. Use -a, -b, -r, or -w.')
        return

    bitsizes.sort()

    run_bits: Dict[int, int] = {}
    for key_length in bitsizes:
        if key_length not in cm.config['auth_bitsizes']:
            print(f'Bitsize {key_length} is not enabled. Available: {cm.config["auth_bitsizes"]}')
            return
        run_bits[key_length] = run_bits.get(key_length, 0) + 1

    candidates: List[Optional[Path]] = []
    for key_length, count in run_bits.items():
        candidates.extend([cm.generate_candidates(key_length, count) for _ in range(count)])

    screened_file_path = cm.config["config_dir"] / 'screened-files.txt'
    with screened_file_path.open('a') as cf:
        for candidate in candidates:
            if candidate:
                cf.write(f'Screened File: {cm.get_screened_path(candidate)}\n')

    for candidate in candidates:
        if candidate:
            cm.screen_candidates(candidate)

    cm.create_moduli_file()


if __name__ == '__main__':
    main()
