from z3 import *

file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	matrix = []
	for line in f:
		matrix.append([int(x) for x in line.split()])
            
n = 3  # the size of the grid
grid = [[Int(f"grid_{i}_{j}") for j in range(n)] for i in range(n)]

# Ensure each row and column contains distinct values
for i in range(n):
    row = [grid[i][j] for j in range(n)]
    col = [grid[j][i] for j in range(n)]
    # make sure each row and column contains unique values
    distinct_row = Distinct(row)
    distinct_col = Distinct(col)

# Add the ordering constraints
all_vars = [grid[i][j] for i in range(n) for j in range(n)]
ordered_vars = [ i*n + j+1 for j in range(n) for i in range(n)]
for i in range(n):
    for j in range(n):
        # Ensure each cell in the grid contains the correct value
        cell_value = If(grid[i][j] == ordered_vars[i * n + j], True, False)
# Define the rotations
rotations = list(range(n))
for i in range(n):
    for j in range(n):
        # Rotate the ith row left by j
        left_rotation = RotateLeft([grid[i][k] for k in rotations], j)
        # Rotate the ith row right by j
        right_rotation = RotateRight([grid[i][k] for k in rotations], j)
        # Rotate the jth column up by i
        up_rotation = RotateLeft([grid[k][j] for k in rotations], i)
        # Rotate the jth column down by i
        down_rotation = RotateRight([grid[k][j] for k in rotations], i)
# Define the objective
objective = [distinct_row, distinct_col, cell_value]
for rotation in [left_rotation, right_rotation, up_rotation, down_rotation]:
    objective += [Distinct(rotation)]
# Solve the problem
s = Solver()
s.add(objective)
if s.check() == sat:
    m = s.model()
    solution = [m]
