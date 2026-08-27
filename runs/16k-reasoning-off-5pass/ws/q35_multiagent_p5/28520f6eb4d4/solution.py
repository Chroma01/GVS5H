import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    X = []
    H = []
    for _ in range(N):
        x_val = int(next(iterator))
        h_val = int(next(iterator))
        X.append(x_val)
        H.append(h_val)

    # Function to check if all buildings are visible at height h
    # Returns True if all visible, False if at least one is hidden
    def check(h):
        # We need to check if for all buildings i, there exists a point y in [0, H[i]]
        # such that for all j < i, the line from (0, h) to (X[i], y) does not intersect building j.
        # The condition for building j NOT blocking the view to (X[i], y) is:
        # Y(X[j]) < H[j]  (strictly less to avoid touching/intersecting)
        # This leads to y < R_j(i, h) where R_j(i, h) = (X[i]/X[j])*H[j] + h*(1 - X[i]/X[j])
        # Building i is visible if min_{j < i} R_j(i, h) > 0.
        # All buildings are visible if for all i, min_{j < i} R_j(i, h) > 0.
        
        # We want to find if there exists any building i such that min_{j < i} R_j(i, h) <= 0.
        # If such a building exists, then not all buildings are visible -> return False.
        # Otherwise, return True.
        
        # To do this efficiently, we can track the minimum R value encountered so far for each "target" building?
        # No, R depends on the target building i.
        # R_j(i, h) = H[j] * (X[i]/X[j]) + h * (1 - X[i]/X[j])
        #           = (H[j] - h) * (X[i]/X[j]) + h
        
        # For a fixed h, we iterate through buildings i from 1 to N-1 (0-indexed).
        # For each i, we need min_{j < i} R_j(i, h).
        # Let's rewrite R_j(i, h):
        # R_j(i, h) = X[i] * (H[j] - h) / X[j] + h
        
        # We want to know if min_{j < i} R_j(i, h) <= 0 for any i.
        # min_{j < i} R_j(i, h) = X[i] * min_{j < i} ( (H[j] - h) / X[j] ) + h
        
        # Let V_j(h) = (H[j] - h) / X[j].
        # Then min_{j < i} R_j(i, h) = X[i] * (min_{j < i} V_j(h)) + h.
        
        # We can maintain the prefix minimum of V_j(h) as we iterate i.
        
        min_V = float('inf')
        
        # Building 0 (index 0) has no predecessors, so it's always visible.
        # Start checking from building 1 (index 1).
        
        for i in range(1, N):
            # Update min_V with the current building j=i-1's V value
            # Wait, we need min over j < i. So before processing i, we should have included j=i-1.
            # Let's update min_V with building i-1's V value.
            v_prev = (H[i-1] - h) / X[i-1]
            if v_prev < min_V:
                min_V = v_prev
            
            # Now min_V is min_{j < i} V_j(h)
            # Calculate min R for building i
            min_R_i = X[i] * min_V + h
            
            if min_R_i <= 0:
                # Building i is hidden (or barely visible with 0 height point, but strict inequality needed)
                # Since we need y > 0 for a valid point on the building (height must be non-negative, but point must be on building)
                # Actually, if min_R_i <= 0, then for all y >= 0, y >= min_R_i is not sufficient to satisfy y < R_j for all j?
                # Condition: exists y in [0, H[i]] such that y < R_j for all j.
                # This requires min_{j} R_j > 0.
                # If min_R_i <= 0, then no such y exists (since y >= 0).
                return False
        
        return True

    # Binary search for the maximum h such that check(h) is False.
    # check(h) is False means not all buildings are visible.
    # check(h) is monotonic: if check(h) is False, then check(h') is False for h' < h?
    # Let's verify monotonicity.
    # As h increases, V_j(h) = (H[j] - h)/X[j] decreases.
    # So min_V decreases.
    # min_R_i = X[i] * min_V + h.
    # The term X[i]*min_V decreases, and h increases.
    # The derivative of min_R_i with respect to h is 1 + X[i] * d(min_V)/dh.
    # d(V_j)/dh = -1/X[j].
    # So d(min_R_i)/dh = 1 - X[i]/X[j] for the active j.
    # Since X[i] > X[j], this derivative is negative.
    # So min_R_i is a decreasing function of h.
    # If min_R_i <= 0 at some h, it will be <= 0 for all larger h.
    # So if check(h) is False (some building hidden), then check(h') is False for all h' > h.
    # This means the set of h where check(h) is False is an interval [0, h_max].
    # We want the maximum h such that check(h) is False.
    
    # Check if all buildings are visible at h=0.
    if check(0):
        print("-1")
        return

    low = 0.0
    high = 2.0 * 10**9 + 7.0 # Sufficiently large upper bound
    
    # Binary search for 100 iterations for high precision
    for _ in range(100):
        mid = (low + high) / 2.0
        if check(mid):
            # All buildings visible at mid, so we need to go lower to find where they become hidden.
            # We want max h where NOT all visible.
            # If all visible at mid, then the threshold is below mid.
            high = mid
        else:
            # Not all visible at mid, so mid is a candidate. Try higher.
            low = mid
            
    print(f"{low:.20f}")

solve()