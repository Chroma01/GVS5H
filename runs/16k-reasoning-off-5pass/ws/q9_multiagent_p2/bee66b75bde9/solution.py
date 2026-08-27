import sys
from bisect import bisect_left

# Increase recursion depth just in case, though we use iterative approach
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

    # Data structures to store constraints
    # lb_map: column -> max row index of a black cell in that column
    lb_map = {}
    
    # row_constraints: row index -> (max_col_of_black, min_col_of_white)
    # If no black cells in row, max_col_of_black = 0
    # If no white cells in row, min_col_of_white = N + 1
    row_constraints = {}
    
    # Set of critical x values for the sweep-line algorithm
    # Includes all row indices with constraints and all LB values
    critical_x = set()
    critical_x.add(N + 1) # Sentinel
    
    for _ in range(M):
        try:
            x = int(next(iterator))
            y = int(next(iterator))
            c = next(iterator)
        except StopIteration:
            break
        
        if c == 'B':
            # Black cell at (x, y)
            # Update LB[y]
            if y not in lb_map or x > lb_map[y]:
                lb_map[y] = x
            
            # Update row constraint L_x (max column of black)
            if x not in row_constraints:
                row_constraints[x] = (0, N + 1)
            if y > row_constraints[x][0]:
                row_constraints[x] = (y, row_constraints[x][1])
        else:
            # White cell at (x, y)
            # Update row constraint U_x (min column of white)
            if x not in row_constraints:
                row_constraints[x] = (0, N + 1)
            if y < row_constraints[x][1]:
                row_constraints[x] = (row_constraints[x][0], y)
            
            # Add row index to critical points
            critical_x.add(x)
            
            # Add LB[y] to critical points if it's > 0
            # We only care about LB values >= 1 for the range [1, N]
            if y in lb_map:
                val = lb_map[y]
                if val > 0:
                    critical_x.add(val)
    
    # Prepare LB values for binary search
    # We need to count how many columns have LB[c] >= x
    # Collect all non-zero LB values
    lb_values = sorted(list(lb_map.values()))
    
    # Helper to get MinK_x = count(c such that LB[c] >= x)
    def get_min_k(x):
        if x <= 0:
            return len(lb_values)
        # bisect_left returns the first index where element >= x
        # Since list is sorted ascending, elements from idx to end are >= x
        idx = bisect_left(lb_values, x)
        return len(lb_values) - idx

    # Sort critical points descending
    sorted_critical = sorted(list(critical_x), reverse=True)
    
    possible = True
    k_after = 0 # Represents k_{x+1} initially for x = N+1
    
    for p in sorted_critical:
        # Calculate MinK for current p
        mk = get_min_k(p)
        
        # Retrieve constraints for row p
        if p in row_constraints:
            L_p, min_y_white = row_constraints[p]
            # U_p is the max allowed width for row p
            # Condition: width < min_y_white => width <= min_y_white - 1
            U_p = min_y_white - 1
        else:
            # No constraints on this row
            L_p = 0
            U_p = N # Width can be at most N
        
        # Calculate k_p
        # We need k_p >= L_p
        # We need k_p >= mk (MinK_p)
        # We need k_p >= k_{p+1} (which is k_after updated for the interval)
        
        # First, determine k_{p+1}
        # In the interval (next_critical, p], MinK is constant = mk.
        # So k_{p+1} = max(mk, k_after)
        k_next = mk if mk > k_after else k_after
        
        # Then k_p = max(L_p, mk, k_next)
        # Note: max(L_p, mk, k_next) is equivalent to max(L_p, mk, max(mk, k_after))
        # which simplifies to max(L_p, mk, k_after)
        
        k_p = L_p if L_p > mk else mk
        if k_p < k_after:
            k_p = k_after
            
        # Check if valid
        if k_p > U_p:
            possible = False
            break
        
        # Update k_after for the next iteration (which will be for a smaller p)
        k_after = k_p
        
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()