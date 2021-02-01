#!/usr/bin/python3

from os import stat
import numpy as np

list2str = lambda l: ''.join(map(str,l))

num_bits = stat('provided/signal.ham').st_size*8//16 # 8 bits per byte, 16-bit float value = 1 bit
raw = [0 if x<0 else 1 for x in np.fromfile('provided/signal.ham', dtype=np.float16)[:160]]
l = 3 # block length
while num_bits%l:
	l += 1
for k in range(3,l):
	s = list()
	for i in range(0,len(raw)-l,l):
		s += raw[i:i+l][:k]
	print('[%i,%i]: %s'%(l,k,''.join([chr(int(list2str(s[i:i+8]),2)) for i in range(0,len(s),8)])))

l = 17
k = 11

for i in range(0,len(raw)-l,l):
	print(raw[i:i+l])