#!/usr/bin/env python
from argparse import ArgumentParser
from pathlib import PosixPath as Path


def args():
    parser = ArgumentParser(description='Moduli In File')
    parser.add_argument('-f', '--file', type=str, default='/etc/ssh/moduli',
                        help='moduli_infile -f <moduli_file')
    return parser.parse_args()


def moduli_infile(infile):
    authorized_bitsizes = (2047, 3071, 4095, 6143, 7679, 8191)
    bitsizes = {}
    for bs in authorized_bitsizes:
        bitsizes[str(bs)] = 0

    lines = infile.read_text().split('\n')
    for line in lines:
        if line.startswith('#') or line.startswith(' '):
            continue
        # Skip Comment and Blank Lines, Bypasses MODULI Header Line
        if line:
            bitsizes[line.split(' ')[4]] += 1

    return bitsizes


def main():
    largs = args()
    freq_table = moduli_infile(Path(largs.file))
    print(f'\nModulus Frequency of {largs.file}:')
    print(f'Mod  Count')
    for modulus in freq_table:
        print(modulus, freq_table[modulus])


if __name__ == '__main__':
    exit(main())
