def export_bash_builder():
    print('''#!/usr/bin/env bash

NICE="nice +15"
GEN_MODULI="python -m moduli_assembly"
GEN_OPTS="-b 3072 4096 6144 7680 8192"


# Four Runs of ssh-keygen Per Bitsize will generate a file with sufficient entries per bitsize (~80)

for ((ii = 0; i < 4; i++)); do
    ${NICE} ${GEN_MODULI} ${GEN_OPTS}
done

''')


def export_csh_builder():
    print('''#!/usr/bin/env csh
set NICE="nice +15"
set GEN_MODULI="python -m moduli_assembly"
set GEN_OPTS="--all"

# Four Runs of ssh-keygen Per Bitsize will generate a file with sufficient entries per bitsize (~80)

foreach run ( 0 1 2 3 )
    $NICE $GEN_MODULI $GEN_OPTS >>& all.gen.log&
end
''')


def export_moduli_infile():
    print('''#!/usr/bin/env bash

WCL="/usr/bin/wc -l"
GREP=/usr/bin/grep
MODULI_FILE=${1:-/etc/ssh/moduli}

echo "\nProcessing Moduli File: ${MODULI_FILE}"

for moduli in 2047 3071 4095 6143 7679 8191
do
    count=`$GREP " $moduli " $MODULI_FILE | $WCL`
    echo "${moduli}: ${count}"
done

''')
