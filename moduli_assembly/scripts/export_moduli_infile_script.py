#!/usr/bin/env python

print('''#!/bin/bash

WCL="/usr/bin/wc -l"
GREP=/usr/bin/grep
MODULI_FILE=${1:-/etc/ssh/moduli}

for moduli in 2047 3071 4095 6143 7679 8191
do
	$GREP " $moduli " $MODULI_FILE | $WCL
done

''')
