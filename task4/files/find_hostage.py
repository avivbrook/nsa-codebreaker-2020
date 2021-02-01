#!/usr/bin/python3

import sys
from json import load
import networkx as nx
from geopandas import read_file
from momepy import gdf_to_nx
import matplotlib.pyplot as plt

GREEN = '#00ff00'
RED = '#ff0000'
BLOCK = 100.0 # block size in metres
AVES = [chr(c) for c in range(ord('A'),ord('V')+1)]
ST_SUFS = ['st','nd','rd']+['th']*15

with open('provided/stepinator.json') as f:
	a = load(f) # acceleration data
v = [0.0] # speed data
disp = [0.0] # displacement data
for ax in a:
	disp.append(v[-1]+0.5*ax)
	v.append(v[-1]+ax)

G = gdf_to_nx(read_file('maps/city-shapefile/edges.shp'))

def tup_scalar_mul(scalar, tup):
	return tuple(x*scalar for x in tup)

def add_tups(tup1, tup2):
	return tuple(map(lambda x,y: x+y, tup1, tup2))

class Path:
	def __init__(self, t, pos, d, visited):
		self.t = t # time
		self.pos = pos # position
		self.d = d # direction vector
		self.visited = visited # visited nodes

def node_colour(node, t):
	return GREEN if (t%60 < 30 and node[0]%400 < 200) or (t%60 >= 30 and node[0]%400 >= 200) else RED

def is_green(node, t, d):
	colour = node_colour(node, t)
	return True if (colour == GREEN and d[1]) or (colour == RED and d[0]) else False

def explore(paths):
	for path in paths:
		if path.t < len(a):
			return path
	return None

def next_node(path, paths):
	m = len(a)
	if path.t > m:
		raise ValueError('no data for this time')
	
	disp_from_prev = abs(path.pos[0]-path.visited[-1][0])%int(BLOCK) if path.d[0] else abs(path.pos[1]-path.visited[-1][1])%int(BLOCK)
	if disp_from_prev >= BLOCK:
		raise ValueError('displacement from previous node must be < %f'%BLOCK)

	t_stopped = t_slowed = 0
	while disp_from_prev < BLOCK and path.t < m:
		disp_from_prev += disp[path.t]
		path.t += 1
		if not t_stopped and round(v[path.t], 2) == 0.0:
			t_stopped = path.t
		elif path.t < m:
			if not t_slowed and a[path.t] < 0.0:
				t_slowed = path.t
			elif t_slowed and a[path.t] > 0.0 and a[path.t-1] < 0.0:
				t_slowed = path.t

	extra = 0.0
	if disp_from_prev >= BLOCK:
		extra = disp_from_prev - BLOCK
		if extra >= BLOCK:
			raise ValueError('too fast')
		disp_from_prev = BLOCK

	path.pos = add_tups(path.visited[-1], tup_scalar_mul(disp_from_prev, path.d))

	if disp_from_prev < BLOCK:
		path.pos = tuple(round(x/BLOCK) * BLOCK for x in path.pos)

	if t_stopped and not t_slowed and is_green(path.pos, t_stopped, path.d):
		paths.remove(path)
		return explore(paths)
	
	must_turn = t_slowed and is_green(path.pos, t_slowed, path.d)

	path.visited.append(path.pos)

	if disp_from_prev < BLOCK:
		if not is_green(path.pos, path.t, path.d):
			paths.remove(path)
	else:
		for x,y in list(G.__getitem__(path.pos)):
			if (x,y) not in path.visited:
				d = tuple(1 if u > p else -1 if u < p else 0 for u,p in zip((x,y), path.pos))
				good = False
				if t_stopped:
					if not is_green(path.pos, t_stopped, path.d):
						good = True
				elif t_slowed and must_turn:
					if d != path.d:
						good = True
				elif d == path.d and is_green(path.pos, path.t, d):
					good = True
				if good:
					paths.append(Path(t=path.t, pos=add_tups(path.pos, tup_scalar_mul(extra, d)), d=d, visited=path.visited.copy()))
		paths.remove(path)

	return explore(paths)

def intersection_to_pos(intr):
	return AVES.index(intr[0])*BLOCK, (intr[1]-1)*BLOCK

def pos_to_intersection(pos):
	st = int(path.pos[1]/BLOCK)+1
	return AVES[int(pos[0]/BLOCK)], str(st)+ST_SUFS[st-1]

if len(sys.argv) != 3:
    print('USAGE: %s avenue street'%sys.argv[0])
    exit(1)

intr = (sys.argv[1], int(sys.argv[2]))
print('Kidnapped at Ave %s & %i%s St'%(intr[0],intr[1],ST_SUFS[intr[1]-1]))

pos = intersection_to_pos(intr)
curr_path = Path(t=0, pos=pos, d=(1,0), visited=[pos])
paths = [curr_path]

while curr_path:
	curr_path = next_node(curr_path, paths)

if len(paths) != 1:
	raise ValueError('found more than one path')
path = paths[0]

intr = pos_to_intersection(path.pos)
print('Hostage taken to Ave', intr[0], '&', intr[1], 'St')

plt.figure(figsize=(10,10))
nx.draw(G, pos={n:n for n in G.nodes()}, node_size=100, node_color=[node_colour(n, path.t) for n in G.nodes()], width=3)

Gp = nx.DiGraph()
if len(path.visited) > 1:
	for n in range(len(path.visited)-1):
		Gp.add_edge(path.visited[n], path.visited[n+1])
else:
	Gp.add_node(path.visited[-1])
nx.draw(Gp, pos={n:n for n in Gp.nodes()}, arrowstyle='->', node_size=125, node_color=['#800080' if node==path.pos else '#000000' for node in Gp.nodes()], edge_color='#800080', width=4)
plt.savefig('path.png')