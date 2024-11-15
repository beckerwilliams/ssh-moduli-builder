#!/usr/bin/env python

def main():
    """

    :return: Text of Bash Shell Moduli Builder
    :rtype: text
    """
    print('''#!/usr/bin/env csh
    
    set NICE="nice +15"
    set GEN_MODULI="python -m moduli_assembly"
    set GEN_OPTS="--all"
    
    # Four Runs of ssh-keygen Per Bitsize will generate a file with sufficient entries per bitsize (~80)
    
    foreach run ( 0 1 2 3 )
        $NICE $GEN_MODULI $GEN_OPTS >>& all.gen.log&
    end
    ''')


if __name__ == '__main__':
    exit(main())
