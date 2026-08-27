import sys

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

    # Dictionaries to store min and max bounds for rows and columns
    # R_min[r] = minimum number of black cells in row r
    # R_max[r] = maximum number of black cells in row r
    # C_min[c] = minimum number of black cells in column c
    # C_max[c] = maximum number of black cells in column c
    
    R_min = {}
    R_max = {}
    C_min = {}
    C_max = {}
    
    # Initialize defaults for rows and columns that appear in input
    # We will update them as we process cells
    
    white_cells = []
    
    for _ in range(M):
        r = int(next(iterator))
        c = int(next(iterator))
        color = next(iterator)
        
        # Initialize bounds if not present
        if r not in R_min:
            R_min[r] = 0
            R_max[r] = N
        if c not in C_min:
            C_min[c] = 0
            C_max[c] = N
            
        if color == 'B':
            # Black cell at (r, c) implies R_r >= c and C_c >= r
            if c > R_min[r]:
                R_min[r] = c
            if r > C_min[c]:
                C_min[c] = r
        else:
            # White cell at (r, c) implies R_r < c and C_c < r is NOT required individually,
            # but R_r <= c-1 OR C_c <= r-1.
            # This gives upper bounds: R_r <= c-1 and C_c <= r-1 are potential constraints.
            # Specifically, R_max[r] = min(R_max[r], c-1)
            # C_max[c] = min(C_max[c], r-1)
            if c - 1 < R_max[r]:
                R_max[r] = c - 1
            if r - 1 < C_max[c]:
                C_max[c] = r - 1
                
            white_cells.append((r, c))

    # Check consistency of bounds for each row
    for r in R_min:
        if R_min[r] > R_max[r]:
            print("No")
            return

    # Check consistency of bounds for each column
    for c in C_min:
        if C_min[c] > C_max[c]:
            print("No")
            return

    # Check white cell conditions
    # For each white cell (r, c), we need R_r < c OR C_c < r.
    # If we choose minimal valid R_r = R_min[r] and C_c = C_min[c],
    # the condition becomes R_min[r] < c OR C_min[c] < r.
    # If this fails, i.e., R_min[r] >= c AND C_min[c] >= r, then it's impossible.
    
    for r, c in white_cells:
        # Get bounds for this row and column
        # Note: r and c are guaranteed to be in the dictionaries because they came from input
        r_min_val = R_min[r]
        c_min_val = C_min[c]
        
        if r_min_val >= c and c_min_val >= r:
            print("No")
            return

    print("Yes")

if __name__ == '__main__':
    solve()