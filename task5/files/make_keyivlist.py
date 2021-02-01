#!/usr/bin/python3

import sys

if len(sys.argv) != 2:
    print('USAGE: %s outputfile'%sys.argv[0])
    exit(1)

with open(sys.argv[1], 'w') as f:
    for mm in ['%02d'%m for m in range(60)]:
        K = (('05'+mm)*4).encode('utf-8').hex()
        for mmm in ['%02d'%m for m in range(60)]:
            iv = ('0'+('024'+mmm)*3).encode('utf-8').hex()
            print(K, iv, file=f)
