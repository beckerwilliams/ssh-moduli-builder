# tldr;

You're here - ok - here's the rationale.

SSHDs installation contains a file of random moduli (safe primes) across a set of modulus key lengths.
These moduli provide the basis for SSHDs session keys.

When using SSH, the pragmatic reality is that most system admins use whatever moduli file
arrives with their platform distribution. As keying material, it's certainly no longer random if it's distributed.
This is Challenge #1.

While OpenSSH provides `ssh-keygen` from which to build moduli files,
`ssh-keygen` requires separate execution for generation and then _safe prime_
screening of the generated candidates.
This is Challenge #2

A well constructed `ssh/moduli` file will contain a sufficient (approximately 80)
'safe-primes' for each of five* modulus key lengths: 3072, 4096, 6144, 7680, and 8192.
After Candidate Generation and Safe Prime Screening, each set of safe-primes have to be concatenated and placed in the
final ssh/moduli filee.
This is Challenge #3

\*Bitlengths < 3071 are DROPPED - Reference `Hardening`

## Quick Start

`moduli-assembly` provides functionality in-module and via exportable shell scripts to generate complete moduli files
with
five steps:

Preparation: Download project Wheel from GitHub

`curl -G
https://github.com/beckerwilliams/ssh-moduli-builder/raw/main/dist/moduli_assembly-0.8.3-py3-none-any.whl
-o moduli_assembly-0.9.7-py3-none-any.whl`

### Create and/or Startup Python venv

`python -m venv .venv`

`source .venv/bin/activate`

### Install moduli-assembly _wheel_

`pip install moduli_assembly-0.9.7-py3-none-any.whl`

### Export Bash Build Script

`python -m moduli_assembly.scripts.export_bash_builder > moduli_builder.sh`

### Make Shell Script Executable

`chmod +x moduli_builder.sh`

####Start Moduli Builder

`./moduli_builder.sh > mod.gen.log 2>&1 &`

### When Complete, Check Frequency Distributio of Created Moduli

`python -m moduli_assembly.scripts.moduli_infile -f ${MODULI-ASSEMBLY-DIR}/MODULI_FILE`

- where ${MODULI-ASSEMBLY} is ${HOME}/.moduli-assembly by default

`





