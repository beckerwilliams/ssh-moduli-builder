#!/bin/bash

NICE="nice +15"
GEN_MODULI=bin/generate_moduli.py
GEN_OPTS="-b 2048 3072 4096 6144 7680 8192"

# Four Runs of ssh-keygen Per Bitsize will generate a file with sufficient entries per bitsize (~80)

for ((ii = 0; i < 4; i++)); do
  $NICE $GEN_GEN_MODULI $GEN_OPTS
done
