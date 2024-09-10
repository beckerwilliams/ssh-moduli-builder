#!/usr/bin/env python3
from pathlib import PosixPath as Path
from argparse import ArgumentParser




def mi_args():
    parser = ArgumentParser(description='SSH Moduli Modulus Distribution')
    parser.add_argument('modulus', type=str, default="/etc/ssh/moduli")
    return parser.parse_args()


def moduli_infile(file='/etc/ssh/moduli'):
    bit_sizes = {"2047": 0, "3071": 0, "4095": 0, "6143": 0, "7679": 0, "8191": 0}
    mod_file = Path(file)
    mod_lst = mod_file.read_text().split('\n')

    for line in mod_lst:
        if line.startswith('#') or line.startswith(' '):
            continue
        keylength = line.split(' ')
        if keylength[4] in bit_sizes:
            bit_sizes[keylength[4]] += 1

    return bit_sizes, mod_file


if __name__ == '__main__':
    args = mi_args()
    (counts, fn) = moduli_infile(args.modulus)
    print(f'Moduli in {fn}:')
    for count in counts:
        print(f'\t{count}: {counts[count]}')
