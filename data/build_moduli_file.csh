#!/bin/csh

set NICE="nice +15"
set GEN_MODULI=bin/generate_moduli.py
set GEN_OPTS="-b 2048 3072 4096 6144 7680 8192"

# Four Runs of ssh-keygen Per Bitsize will generate a file with sufficient entries per bitsize (~80)

foreach run ( 0 1 2 3 )
    $NICE $GEN_MODULI $GEN_OPTS
end