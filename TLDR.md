# tldr;

You're here - ok - here's the rationale.

SSHDs installation contains a file of random moduli (safe primes) across a set of modulus keylengths.
These moduli provide the basis for SSHDs session keys.

When using SSH, the pragmatic reality is that most sys admins use whatever moduli file 
arrives with their platform distribution. As  keying material, it's certainly no longer random if it's distributed.
This is Challene #1.

While OpenSSH provides `ssh-keygen` from which to build moduli files,
`ssh-keygen` requires separate execution for generation and then _safe prime_
screening of the generated candidates.
This is Challenge #2

A well constructed `ssh/moduli` file will contain a sufficient (approximately 80) 
'safe-primes' for each of six modulus keylengths: 2048, 3072, 4096, 6144, 7680, and 8192.
After Candidate Generation and Safe Prime Screening, each set of safe-primes have to be concatenated and placed in the final ssh/moduli filee.
This is Challenge #3

## Quick Start
`moduli-assembly` provides functionality in-module and via exportable shell scripts to generate complete moduli files with
five steps:

1. Create and/or Startup Python venv

`python -m venv .venv`

`source .venv/bin/activate`

2. Install moduli-assembly _wheel_

`pip install moduli_assembly-x.x.x.whl`

3. Export Bash Build Script

`python -m moduli_assembly.scripts.export_bash_builder > moduli_builder.sh`

4. Make Shell Script Executable

`chmod +x moduli_builder.sh`

5. Start Moduli Builder

`./moduli_builder.sh > mod.gen.log 2>&1 &`

6. When Complete, Check Frequency Distributio of Created Moduli

`python -m moduli_assembly.scripts.moduli_infile -f ./MODULI_PROTO

`




