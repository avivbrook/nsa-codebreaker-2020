#!/usr/bin/python3

import sys

if len(sys.argv) != 2:
    print('USAGE: %s outputfile' % sys.argv[0])
    exit(1)

with open(sys.argv[1], 'w') as f:
    for name in ['Zara', 'zara']:
        for delim1 in ['', '-', ' ']:
            for month in ['Sep', 'sep', '09', '9']:
                for delim2 in ['', '-', ' ']:
                    print(name+delim1+month+delim2+'10\n'+name+delim1+'10'+delim2+month, file=f)