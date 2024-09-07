#!/usr/bin/env python
from pathlib import PosixPath as Path

with Path.home().joinpath('build_moduli_file.sh').open('w') as mf:
    with Path('../data/build_moduli_file.sh') as sf:
        mf.write(sf.read_text())
