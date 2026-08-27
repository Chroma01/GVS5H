import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Dictionary to store constraints for each row
    # row_constraints[r] = {'L': lower_bound, 'U': upper_bound}
    # L represents the minimum number of black cells required in row r (from Black constraints)
    # U represents the maximum number of black cells allowed in row r (from White constraints)
    row_constraints = {}

    for _ in range(M):
        try:
            x = int(next(iterator))
            y = int(next(iterator))
            c = next(iterator)
        except StopIteration:
            break

        if x not in row_constraints:
            row_constraints[x] = {'L': 0, 'U': N}
        
        if c == 'B':
            # If cell (x, y) is Black, then row x must have at least y black cells.
            # So R_x >= y.
            row_constraints[x]['L'] = max(row_constraints[x]['L'], y)
        else:
            # If cell (x, y) is White, then row x must have fewer than y black cells.
            # So R_x < y => R_x <= y - 1.
            row_constraints[x]['U'] = min(row_constraints[x]['U'], y - 1)

    # Get all unique rows involved and sort them
    sorted_rows = sorted(row_constraints.keys())

    # We need to find a sequence R_1, ..., R_N such that:
    # 1. L_r <= R_r <= U_r for all r
    # 2. R_1 >= R_2 >= ... >= R_N (Monotonicity condition derived from the problem structure)
    #
    # We can determine the maximum possible value for R_r given the prefix constraints.
    # Let U'_r be the tightest upper bound for R_r considering R_1 >= ... >= R_r.
    # U'_r = min(U_r, U'_{r-1}) with U'_0 = N.
    # A valid sequence exists if and only if L_r <= U'_r for all r.
    
    current_max_U = N
    
    for r in sorted_rows:
        constraints = row_constraints[r]
        L = constraints['L']
        U = constraints['U']
        
        # Check immediate consistency for this row
        if L > U:
            print("No")
            return
        
        # Propagate the upper bound from previous rows
        # The current row's R_r cannot exceed the upper bound established by the previous row (R_{r-1})
        current_max_U = min(current_max_U, U)
        
        # Check if the lower bound is compatible with the propagated upper bound
        if L > current_max_U:
            print("No")
            return
        
        # current_max_U is now the effective upper bound for row r.
        # For the next row r_next (where r_next > r), the constraint will be R_{r_next} <= R_r.
        # So the upper bound for r_next will be min(U_{r_next}, current_max_U).
        # We keep current_max_U as is for the next iteration.
        
    print("Yes")

if __name__ == '__main__':
    solve()