#!/usr/bin/python3

import numpy as np
from collections import Counter
import json

list2str = lambda l: ''.join(map(str,l))

n = 16
k = 11
p = 1

print('Reading from file...', end='', flush=True)
raw = [0 if x<0 else 1 for x in np.fromfile('provided/signal.ham', dtype=np.float16)]
print(' done', flush=True)

d = list()
for i in range(k):
	d.append(Counter())

for i in range(0,len(raw)-n-p,n+p):
    block = raw[i:i+n+p]
    data = block[:k]
    par = block[k:n]
    if data.count(1) == 1:
    	d[data.index(1)][list2str(par)] += 1

P = list()
for row in d:
	P.append(list(int(x) for x in row.most_common(1)[0][0]))

G = np.append(np.identity(k, dtype=np.int), P, axis=1)
print('\ngenerator matrix G', G, sep='\n', flush=True)
H = np.append(np.transpose(P), np.identity(n-k, dtype=np.int), axis=1)
print('\nparity check matrix H', json.dumps(H.tolist()), sep='\n', flush=True)

synd = """0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0
0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     1
0     0     0     0     0     0     0     0     0     0     0     0     0     0     1     0
1     0     0     0     0     0     1     0     0     0     0     0     0     0     0     0
0     0     0     0     0     0     0     0     0     0     0     0     0     1     0     0
1     0     1     0     0     0     0     0     0     0     0     0     0     0     0     0
1     0     0     0     0     0     0     0     0     0     0     0     1     0     0     0
0     0     0     0     0     1     0     0     0     0     0     0     0     0     0     0
0     0     0     0     0     0     0     0     0     0     0     0     1     0     0     0
1     0     0     0     0     1     0     0     0     0     0     0     0     0     0     0
1     0     0     0     0     0     0     0     0     0     0     0     0     1     0     0
0     0     1     0     0     0     0     0     0     0     0     0     0     0     0     0
1     0     0     0     0     0     0     0     0     0     0     0     0     0     1     0
0     0     0     0     0     0     1     0     0     0     0     0     0     0     0     0
1     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0
1     0     0     0     0     0     0     0     0     0     0     0     0     0     0     1
0     0     0     0     0     0     0     0     0     0     0     1     0     0     0     0
1     0     0     0     1     0     0     0     0     0     0     0     0     0     0     0
1     0     0     0     0     0     0     1     0     0     0     0     0     0     0     0
0     0     0     0     0     0     0     0     1     0     0     0     0     0     0     0
1     0     0     0     0     0     0     0     0     0     1     0     0     0     0     0
0     0     0     1     0     0     0     0     0     0     0     0     0     0     0     0
0     1     0     0     0     0     0     0     0     0     0     0     0     0     0     0
1     0     0     0     0     0     0     0     0     1     0     0     0     0     0     0
1     1     0     0     0     0     0     0     0     0     0     0     0     0     0     0
0     0     0     0     0     0     0     0     0     1     0     0     0     0     0     0
0     0     0     0     0     0     0     0     0     0     1     0     0     0     0     0
1     0     0     1     0     0     0     0     0     0     0     0     0     0     0     0
0     0     0     0     0     0     0     1     0     0     0     0     0     0     0     0
1     0     0     0     0     0     0     0     1     0     0     0     0     0     0     0
1     0     0     0     0     0     0     0     0     0     0     1     0     0     0     0
0     0     0     0     1     0     0     0     0     0     0     0     0     0     0     0"""

syndtable = [[int(y) for y in x.split()] for x in synd.splitlines()]

out = ''
for i in range(0,len(raw)-n-p,n+p):
	block = raw[i:i+n+p]
	c = raw[i:i+n]
	syndrome = int(list2str(np.matmul(c,np.transpose(H))%2),2)
	if syndrome:
		err = syndtable[syndrome]
		c = np.add(c,err)%2
	out += list2str(c[:k])

bit_strings = [out[i:i+8] for i in range(0,len(out),8)]
byte_list = [int(b,2) for b in bit_strings]
with open('video.avi', 'wb') as f:
	f.write(bytearray(byte_list))