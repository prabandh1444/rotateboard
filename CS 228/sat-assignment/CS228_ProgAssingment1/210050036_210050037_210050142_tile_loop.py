### TEAM MEMBERS
## MEMBER 1: 210050036
## MEMBER 2: 210050037
## MEMBER 3: 210050142

from z3 import *
import sys

def func(i,j,k,objectives):
	phi = True
	if(j<n):
		if(i == 0):
			for a in range(j):
				for b in range(n):
					phi = And(phi, cells[a][b][k+1] == cells[a][b][k])

			for b in range(n):
				phi = And(phi, cells[j][b][k+1] == cells[j][(b+1)%n][k])

			for a in range(j+1,n):
				for b in range(n):
					phi = And(phi, cells[a][b][k+1] == cells[a][b][k])
		if(i == 1):
			for a in range(j):
				for b in range(n):
					phi = And(phi, cells[a][b][k+1] == cells[a][b][k])

			for b in range(n):
				phi = And(phi, cells[j][b][k+1] == cells[j][(b-1)%n][k])

			for a in range(j+1,n):
				for b in range(n):
					phi = And(phi, cells[a][b][k+1] == cells[a][b][k])
	if(j>=n):
		j = j-n
		if(i == 0):
			for a in range(j):
				for b in range(n):
					phi = And(phi, cells[b][a][k+1] == cells[b][a][k])

			for b in range(n):
				phi = And(phi, cells[b][j][k+1] == cells[(b+1)%n][j][k])

			for a in range(j+1,n):
				for b in range(n):
					phi = And(phi, cells[b][a][k+1] == cells[b][a][k])
		if(i == 1):
			for a in range(j):
				for b in range(n):
					phi = And(phi, cells[b][a][k+1] == cells[b][a][k])

			for b in range(n):
				phi = And(phi, cells[b][j][k+1] == cells[(b-1)%n][j][k])

			for a in range(j+1,n):
				for b in range(n):
					phi = And(phi, cells[b][a][k+1] == cells[b][a][k])
		j += n

	objectives.append(And(moves[i][j][k],phi))
	return

file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	matrix = []
	for line in f:
		matrix.append([int(x) for x in line.split()])

s = Solver()

# Set s to the required formula
cells = [[[Int("cell_%s_%s_%s" % (i, j, k)) for k in range(T+1)] for j in range(n)] for i in range(n)]

moves = [[[Bool("moves_%s_%s_%s" % (i, j, k)) for k in range(T)] for j in range(2*n)] for i in range(2)] 
# (0,j,k) == left/up # (1,j,k) == right/down 
# 0 to n-1 (row) # n to 2n-1 (column)

i_moves = [Bool("i_moves_%s" % (k)) for k in range(T)]
#Identical moves which return the same matrix


# Initial values
for i in range(n):
    for j in range(n):
        s.add(cells[i][j][0] == matrix[i][j])
			
# Restrict Rotations
for k in range(T):
	objectives=[]
	for j in range(2*n):
		func(0,j,k,objectives)      
		func(1,j,k,objectives)
	pi = True
	for a in range(n):
		for b in range(n):
			pi = And(pi, cells[a][b][k+1] == cells[a][b][k])
	objectives.append(And(i_moves[k],pi))
	s.add(PbEq([(obj,1) for obj in objectives],1))

# end clause
for i in range(n):
    for j in range(n):
        s.add(cells[i][j][T] == (n*i+j+1))

# Output the moves	
x = s.check()
print(x)
if x == sat:
	m = s.model()
	
	for k in range(T):
		for i in range(2):
			for j in range(2*n):
				if m[moves[i][j][k]] == True:
					if j < n:
						if i == 0:
							print(str(j)+"l")
						if i == 1:
							print(str(j)+"r")
					else:
						if i == 0:
							print(str(j-n)+"u")
						if i == 1:
							print(str(j-n)+"d")
