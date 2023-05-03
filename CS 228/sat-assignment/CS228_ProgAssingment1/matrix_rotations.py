from z3 import *

# Define the matrix
matrix = [[0, 1, 2], [2, 0, 1], [1, 2, 0]]

# Create a Z3 solver instance
solver = Solver()

# Define the number of rows and columns
num_rows, num_cols = len(matrix), len(matrix[0])

# Create a boolean variable for each entry in the matrix
vars = [[Bool(f"x{i}_{j}") for j in range(num_cols)] for i in range(num_rows)]

# Define a constraint that ensures that each row and each column has exactly one entry that is rotated
for i in range(num_rows):
    solver.add(AtMost(*vars[i], 1))
    solver.add(AtLeast(*vars[i], 1))
    for j1 in range(num_cols):
        for j2 in range(j1 + 1, num_cols):
            solver.add(Or(Not(vars[i][j1]), Not(vars[i][j2])))

for j in range(num_cols):
    solver.add(AtMost(*[vars[i][j] for i in range(num_rows)], 1))
    solver.add(AtLeast(*[vars[i][j] for i in range(num_rows)], 1))
    for i1 in range(num_rows):
        for i2 in range(i1 + 1, num_rows):
            solver.add(Or(Not(vars[i1][j]), Not(vars[i2][j])))

# Define a constraint that enforces the rotation of the first row
rotated = vars[0]
unrotated = [vars[0][j] for j in range(1, num_cols)] + [vars[0][0]]
for i in range(num_rows):
    for j in range(num_cols):
        if j == 0:
            solver.add(Implies(unrotated[i], Not(vars[i][j])))
        else:
            solver.add(Implies(And(unrotated[i], vars[i][j-1]), Not(vars[i][j])))
    solver.add(Implies(rotated[i], Not(unrotated[i])))

# Solve the SAT problem
if solver.check() == sat:
    # Get the solution
    solution = [[0 for j in range(num_cols)] for i in range(num_rows)]
    model = solver.model()
    for i in range(num_rows):
        for j in range(num_cols):
            if is_true(model[vars[i][j]]):
                solution[i][j] = (matrix[i][(j-1)%num_cols] if i == 0 else matrix[(i-1)%num_rows][j])
    print(solution)
else:
    print("Unsatisfiable")
