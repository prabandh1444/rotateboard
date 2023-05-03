#!/usr/bin/python3

from z3 import *
import argparse
import itertools
import time
from subprocess import call

# n is number of nodes
# d is number of colors
#
n = 500
d = 3

# reading edges from a file
# the file has 7000 edges for graph over 500 nodes
edges = []
with open("edges.txt") as f:
    for line in f:
        edges.append([int(v) for v in line.strip().split(',')])

#===================================
start = 1100 # starting number of edges to consider
delta = 10   # consider 10 edges more in each step
limit = 1300 # maximum number of edges to consider
        
# declare variables d color problem n 500 nodes
vs = [ [ Bool("p_{}_{}".format(i,j)) for j in range(d)] for i in range(n)]

# each node has at least one color
Node_Fs = [ Or( vs[i] ) for i in range(n) ]

# neigbouring nodes do not have same color
edge_Fs = []
for e in edges[0:limit]:
    # constraints for a single edge
    edge_cons = [ Or( Not(vs[ e[0] ][j]), Not(vs[ e[1] ][j]) ) for j in range(d)]
    edge_Fs.append( And( edge_cons ) )


edge_num = start
data = open("graph-color.data", "w")
print( "Edges Time Status")

while edge_num < limit:
    st = time.time()
    s = Solver()
    s.add( And(Node_Fs) )
    s.add( And(edge_Fs[0:edge_num]) ) # consider only first edge_num edges
    r = s.check()
    tt = time.time() - st
    data.write( str(edge_num) + " " + str(tt) + " " )
    print( edge_num, end = " ")
    print( tt, end = " ")
    if r == sat:
        data.write( "50\n" )
        print("solved")
    else:
        data.write( "0\n" )
        print("unsolvable")
    edge_num = edge_num + delta
data.close()

call(["gnuplot", "-persist", "graph-color-plot.p"])
