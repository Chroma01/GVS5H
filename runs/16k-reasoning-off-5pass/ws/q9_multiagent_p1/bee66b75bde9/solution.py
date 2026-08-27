import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Dictionary to store constraints for each column
    # col_constraints[c] = {'min_black': max_r, 'max_white': min_r - 1}
    # Initialize with default values: min_black = 0, max_white = N
    col_constraints = {}
    
    unique_cols = set()
    
    for _ in range(M):
        try:
            r = int(next(iterator))
            c = int(next(iterator))
            color = next(iterator)
        except StopIteration:
            break
        
        unique_cols.add(c)
        
        if color == 'B':
            # Black cell at (r, c) implies T_c >= r
            if c not in col_constraints:
                col_constraints[c] = {'min_black': 0, 'max_white': N}
            col_constraints[c]['min_black'] = max(col_constraints[c]['min_black'], r)
        else:
            # White cell at (r, c) implies T_c < r => T_c <= r - 1
            if c not in col_constraints:
                col_constraints[c] = {'min_black': 0, 'max_white': N}
            col_constraints[c]['max_white'] = min(col_constraints[c]['max_white'], r - 1)

    # Check for immediate contradictions within a single column
    for c, constraints in col_constraints.items():
        if constraints['min_black'] > constraints['max_white']:
            print("No")
            return

    # Sort unique columns
    sorted_cols = sorted(list(unique_cols))
    
    # Helper to get L and R for a column index
    def get_L(c):
        if c in col_constraints:
            return col_constraints[c]['min_black']
        return 0
    
    def get_R(c):
        if c in col_constraints:
            return col_constraints[c]['max_white']
        return N

    # We need to check if there exists a non-decreasing sequence T_1, ..., T_N
    # such that L_c <= T_c <= R_c for all c.
    # We process intervals where L and R are constant.
    
    current_T = 0 # Represents T_{prev} (initially T_0 = 0)
    
    # Define intervals
    intervals = []
    if sorted_cols:
        # Interval before the first constrained column
        if sorted_cols[0] > 1:
            intervals.append((1, sorted_cols[0] - 1))
        
        # Intervals between constrained columns
        for i in range(len(sorted_cols) - 1):
            intervals.append((sorted_cols[i], sorted_cols[i+1] - 1))
            
        # Interval after the last constrained column
        if sorted_cols[-1] < N:
            intervals.append((sorted_cols[-1], N))
    else:
        # No columns with constraints
        intervals.append((1, N))
        
    for u, v in intervals:
        L = get_L(u)
        R = get_R(u)
        
        # We need to determine T_u.
        # T_u must be >= current_T (from previous column)
        # T_u must be >= L
        # T_u must be <= R
        
        required_min = max(current_T, L)
        
        if required_min > R:
            print("No")
            return
        
        # Update current_T for the next column
        # Since L is constant in this interval, T will remain constant at required_min
        # throughout the interval [u, v] because T_{i+1} = max(T_i, L) = T_i.
        current_T = required_min
        
    print("Yes")

if __name__ == '__main__':
    solve()