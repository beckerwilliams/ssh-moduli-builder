# SSH Moduli File Generator

Scripts to generate [/usr/local]/etc/ssh/moduli files

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)


## Installation
```pip install ./moduli_assembly-<version>-py3-none-any.whl```

## Usage
```python -m moduli_assembly -a, --all```

Builds SSH Moduli File with All AUthorized Bitsizes: 
- 2048, 3072, 4096, 6144, 7680, 8192

```python -m moduli_assembly -b, --bitsizes <bitsize> [<bitsize> [...]]```
Build Moduli for each bitsize given. Multiple Entries provide Multiple Runs

- example `python -m moduli_assembly --bitsizes 2048 2048 3072 4096`
- _Two Runs of '2048', one of '3072', one of '4096'_

```python -m moduli_assembly -r, --restart```

- example `python -m moduli_assembly --restart`
- _Completes Screening of Any Interrupted Screening Runs_

```python -m moduli_assembly -w, --write```

- example `python -m moduli_assembly --write`
- _Writes out SSH MODULI File from Existing Safe Primes_

## Examples
In order to build a sufficiently diverse SSH Moduli file, we need 4 runs of EACH bitsize.
The following Shell Scripts will start 4 process in parallel, and produce a Complete SSH Moduli File with over 
75 entries for each bitsize.

moduli-assembly will take about 1 Week to produce a complete File on an 4 Core Intel i7 processor.

### Export Shell Scripts
``
#### Export(C Shell (csh) Utility
```python -m moduli_assembly.scripts.export_csh_runner > build_moduli_file.csh```

#### Export Bourne Again Shell (bash)
```python -m moduli_assembly.scripts.export_bash_runner > build_moduli_file.sh```

##### Set Execute Bit on Scripts
`chmod +x ./build_moduli_file.*sh`

##### Run
`./build_moduli_file.[c]sh >& all.gen.log&`

## License
MIT License

Copyright (c) 2024 Ron Williams, General Partner, Becker Williams Trading General Partnership

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


