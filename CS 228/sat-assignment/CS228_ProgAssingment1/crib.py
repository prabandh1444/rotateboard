### TEAM MEMBERS
## MEMBER 1: <roll_number_1>
## MEMBER 2: <roll_number_2>
## MEMBER 3: <roll_number_3>

from z3 import *
import sys
import time
start_time = time.time()

file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	mat = []
	for line in f:
		mat.append([int(x) for x in line.split()])

grid = [[ [ Int("grid_%s_%s_%s" % (i+1, j+1, l+1)) for j in range(n) ]
      for i in range(n) ] for l in range(T+1)]

instance_c = [ grid[0][i][j] == mat[i][j] for i in range(n) for j in range(n) ]

cells_c  = [ And(1 <= grid[l][i][j], grid[l][i][j] <= n**2)
             for i in range(n) for j in range(n) for l in range(T+1)]

# Ensure each row and column contains distinct values
#rows_c   = [ Distinct(grid[l][i][j]) for i in range(n) for j in range(n) for l in range(T) ]

# each column contains a digit at most once

# Add the ordering constraints

ordered_vars = [ i*n + j + 1 for i in range(n) for j in range(n)]

ordering_constraints = [grid[T][i][j] == ordered_vars[i * n + j] for i in range(n) for j in range(n)]

# Define the rotations

row_rot = [[Int("r_%s_%s_%s" % (i+1, j+1, l+1)) for j in range(2) for i in range(n)] for l in range(T)]

col_rot = [ [ Int("c_%s_%s_%s" % (i+1, j+1, l+1)) for j in range(2) for i in range(n)] for l in range(T)]

cells_c1  = [ Or(0 == row_rot[l][i], row_rot[l][i] == 1)
             for i in range(2*n) for l in range(T) ]

cells_c2  = [ Or(0 == col_rot[l][i], col_rot[l][i] == 1)
             for i in range(2*n) for l in range(T) ]

#print(type(cells_c1[1]))
constraints=[Or((sum(row_rot[i]) + sum(col_rot[i])) == 0, (sum(row_rot[i]) + sum(col_rot[i])) == 1) for i in range(T)]

row = []
column = []
no_change = []
shift = []

for l in range(T):
    for i in range(n):
        for j in range(n):
            no_change.append((grid[l][i][j]!=grid[l+1][i][j]) == (Or(row_rot[l][i] == 1, row_rot[l][i+n] == 1, col_rot[l][j] == 1, col_rot[l][j+n] == 1)))
            no_change.append((grid[l][i][j]!=grid[l+1][i][j]) == (Or(grid[l][i][(j+1)%n]==grid[l+1][i][j], grid[l][i][(j-1)%n]==grid[l+1][i][j], grid[l][(i-1)%n][j]==grid[l+1][i][j], grid[l][(i+1)%n][j]==grid[l+1][i][j])))
    for i in range(2*n):
        cribs1 = []
        cribs2 = []
        if i < n:
            x = True
            y = True
            for j in range(n):
                for k in range(n):
                    if j != i:
                        x = And(x, (grid[l+1][j][k] == grid[l][j][k]))
                        y = And(y, (grid[l+1][k][j] == grid[l][k][j]))
                    else:
                        x = And(x, (grid[l+1][j][k] == grid[l][j][(k+1)%n]))
                        y = And(y, (grid[l+1][k][j] == grid[l][(k-1)%n][j]))
            cribs1.append((row_rot[l][i] == 1) == x)
            cribs2.append((col_rot[l][i] == 1) == y)
                #     else:
                #         x = And(x, grid[l+1][i][k] == grid[l][i][(k+1) % n])
                #         y = And(y, grid[l+1][k][i] == grid[l][(k-1) % n][i])
                # cribs1.append(Implies(row_rot[l][i] == 1 , x))
                # cribs2.append(Implies(col_rot[l][i] == 1 , y))
        else:
            a = True
            b = True
            for j in range(n):
                for k in range(n):
                    if j != i-n:
                        a = And(a, (grid[l+1][j][k] == grid[l][j][k]))
                        b = And(b, (grid[l+1][k][j] == grid[l][k][j]))
                    else:
                        a = And(a, (grid[l+1][j][k] == grid[l][j][(k-1)%n]))
                        b = And(b, (grid[l+1][k][j] == grid[l][(k+1)%n][j]))
            cribs1.append((row_rot[l][i] == 1) == a)
            cribs2.append((col_rot[l][i] == 1) == b)
                #     else:
                #         a = And(a, grid[l+1][i-n][k] == grid[l][i-n][(k-1) % n])
                #         b = And(b, grid[l+1][k][i-n] == grid[l][(k+1) % n][i-n])
                # cribs1.append(Implies(row_rot[l][i] == 1 , a))
                # cribs2.append(Implies(col_rot[l][i] == 1 , b))
    row+=cribs1
    column+=cribs2
# Define the objective

# for l in range(T):
#     for i in range(n):
#         for j in range(n):
#             x = (row_rot[l][j] == 1)
#             y = (col_rot[l][j] == 1)
#             z = (row_rot[l][j+n] == 1)
#             w = (col_rot[l][j+n] == 1)
#             for k in range(n):
#                 x = And(x, grid[l+1][j][k] == grid[l][j][(k+1) % n])
#                 y = And(y, grid[l+1][k][j] == grid[l][(k-1) % n][j])
#                 z = And(z, grid[l+1][j][k] == grid[l][j][(k-1) % n])
#                 w = And(w, grid[l+1][k][j] == grid[l][(k+1) % n][j])
#             shift.append((grid[l+1][j][i] == grid[l][j][(i+1) % n]) == x)
#             shift.append((grid[l+1][i][j] == grid[l][(i-1) % n][j]) == y)
#             shift.append((grid[l+1][j][i] == grid[l][j][(i-1) % n]) == z)
#             shift.append((grid[l+1][i][j] == grid[l][(i+1) % n][j]) == w)

nextmove = []
for l in range(T-1):
    for i in range(n):
        nextmove.append(Implies((row_rot[l][i] == 1),(row_rot[l+1][i + n] == 0)))
        nextmove.append(Implies((row_rot[l][i+n] == 1),(row_rot[l+1][i] == 0)))
        nextmove.append(Implies((col_rot[l][i] == 1),(col_rot[l+1][i + n] == 0)))
        nextmove.append(Implies((col_rot[l][i+n] == 1),(col_rot[l+1][i] == 0)))

allset = []
for l in range(T-1):
    x = True
    y = True
    z = True
    for i in range(n):
        for j in range(n):
            z = And(z, grid[l][i][j] == i*n+ j+ 1,grid[l+1][i][j] == i*n+ j+ 1 )
    allset.append(((sum(row_rot[l]) + sum(col_rot[l])) == 0) == z)
    for k in range(l+1, T):
        x = And(x, (sum(row_rot[k]) + sum(col_rot[k])) == 0)
    allset.append(Implies((sum(row_rot[l]) + sum(col_rot[l])) == 0, x))


objective = cells_c + ordering_constraints + constraints + cells_c2 + nextmove + allset
objective += cells_c1 + row + column + instance_c + no_change
# Solve the problem
s = Solver()
s.add(objective)
print(s.check())
total_time = time.time()-start_time
print(total_time)
if s.check() == sat:
    m = s.model()
    print( [[m.eval(row_rot[i][j]).as_long() for j in range(2*n)] for i in range(T)] )
    print( [[m.eval(col_rot[i][j]).as_long() for j in range(2*n)] for i in range(T)] )
    print( [[m.eval(grid[l][i][j]).as_long() for i in range(n) for j in range(n)] for l in range(T+1)] )
#     #solution = [[m.eval(grid[i][j]).as_long() for j in range(n)] for i in range(n)]
#     #print(m.eval(row_rot))
#     #print(m.eval(col_rot))
# else :
#     #print(s.unsat_core)
#     print("unsat")