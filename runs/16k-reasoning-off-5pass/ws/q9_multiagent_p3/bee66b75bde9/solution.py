import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200005)

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

    # Use dictionaries to store constraints for sparse rows (since N can be up to 10^9)
    # low[r] = minimum possible value for L_r (max black col in row r)
    # high[r] = maximum possible value for L_r
    # Default low is 0 (no black cells implies L_r >= 0)
    # Default high is N (no white cells implies L_r <= N)
    
    low = {}
    high = {}
    
    # Process M constraints
    for _ in range(M):
        r = int(next(iterator))
        c = int(next(iterator))
        color = next(iterator)
        
        if color == 'B':
            # If cell (r, c) is Black, then L_r must be at least c.
            if r not in low or c > low[r]:
                low[r] = c
        else:
            # If cell (r, c) is White, then L_r must be strictly less than c.
            # So L_r <= c - 1.
            val = c - 1
            if r not in high or val < high[r]:
                high[r] = val
    
    # Get all unique rows involved in constraints and sort them
    rows = sorted(list(low.keys()) + list(high.keys()))
    
    # Check for immediate contradictions within a single row
    for r in rows:
        l_val = low.get(r, 0)
        h_val = high.get(r, N)
        if l_val > h_val:
            print("No")
            return

    # Forward pass: Compute max possible value for L_r considering constraints from 1 to r.
    # Since L_r <= L_{r-1}, the max value for L_r is min(high[r], max_val_of_L_{r-1}).
    # We track 'current_max_L' which represents the tightest upper bound propagated from row 1.
    current_max_L = N
    
    # We need to store the max_possible value for each constrained row to use in backward pass.
    max_possible_map = {}
    
    # We iterate through the sorted rows.
    # Rows not in the dictionary have low=0, high=N.
    # The 'current_max_L' decreases only when we encounter a row with a constraint.
    # Between two constrained rows r_prev and r_curr, the max_L remains constant (bounded by N).
    # We just need to ensure that at each constrained row, the propagated max_L is >= low[r].
    
    # Forward Pass Logic:
    # current_max_L starts at N.
    # For each row r in sorted order:
    #   current_max_L = min(current_max_L, high[r])
    #   if current_max_L < low[r]: return No
    #   max_possible_map[r] = current_max_L
    
    for r in rows:
        l_val = low[r]
        h_val = high[r]
        
        # Update upper bound
        if h_val < current_max_L:
            current_max_L = h_val
        
        # Check consistency
        if current_max_L < l_val:
            print("No")
            return
        
        max_possible_map[r] = current_max_L

    # Backward Pass Logic:
    # current_min_L starts at 0.
    # For each row r in reverse sorted order:
    #   current_min_L = max(current_min_L, low[r])
    #   if current_min_L > max_possible_map[r]: return No
    
    current_min_L = 0
    for r in reversed(rows):
        l_val = low[r]
        
        # Update lower bound
        if l_val > current_min_L:
            current_min_L = l_val
        
        # Check consistency with forward pass upper bound
        if current_min_L > max_possible_map[r]:
            print("No")
            return

    # If we pass all checks, a valid sequence exists.
    print("Yes")

if __name__ == '__main__':
    solve()