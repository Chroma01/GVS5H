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
        X.append(int(next(iterator)))
        H.append(int(next(iterator)))

    # Check if h=0 is valid (all visible)
    # For h=0, condition for building j: max_{k<j} (H_k * X_j / X_k) <= H_j
    # Let's implement the general check function first
    
    def is_all_visible(h):
        # We need to check if for all j, h + X_j * max_{k<j} ((H_k - h)/X_k) <= H_j
        # Let val_k = (H_k - h) / X_k
        # We maintain max_val = max_{k<j} val_k
        
        # For j=0 (first building), there are no k < j, so max is -inf.
        # Condition: h <= H[0]. If h > H[0], then building 0 is not visible?
        # Wait, the problem says "building i is visible if there exists a point Q on building i...".
        # For the first building, there are no intermediate buildings.
        # The line of sight to the top (X_0, H_0) is clear.
        # So building 0 is always visible regardless of h?
        # Let's re-read carefully: "line segment PQ does not intersect with any *other* building".
        # Since there are no other buildings with index < 0, building 0 is always visible.
        # So for j=0, the condition is vacuously true.
        # My formula L_0(h) = h + X_0 * (-inf) = -inf.
        # Condition: -inf <= H_0, which is always true.
        # So we start with max_val = -infinity.
        
        max_val = -float('inf')
        
        for j in range(N):
            # Before processing building j, max_val is max_{k < j} ((H_k - h)/X_k)
            # Check condition for building j
            # Required: h + X[j] * max_val <= H[j]
            # If max_val is -inf, the term is -inf, so condition holds.
            
            if max_val != -float('inf'):
                required_h = h + X[j] * max_val
                if required_h > H[j]:
                    return False
            
            # Update max_val for next buildings (include current building j)
            val_j = (H[j] - h) / X[j]
            if val_j > max_val:
                max_val = val_j
                
        return True

    # Check h=0
    if is_all_visible(0.0):
        print("-1")
        return

    # Binary search for the maximum h such that NOT all buildings are visible.
    # Since is_all_visible(h) is monotonic (if h is too high, some buildings get blocked),
    # we want the largest h where is_all_visible(h) is False.
    # Actually, let's verify monotonicity.
    # As h increases, (H_k - h)/X_k decreases. So max_val decreases.
    # So h + X_j * max_val might increase or decrease?
    # Let f_j(h) = h + X_j * max_{k<j} ((H_k - h)/X_k).
    # This function is concave and non-decreasing?
    # Actually, let's look at the condition: visible if f_j(h) <= H_j.
    # If h is very large, (H_k - h)/X_k is very negative. max_val is very negative.
    # h + X_j * (very negative) -> -infinity. So f_j(h) -> -infinity.
    # So for very large h, f_j(h) <= H_j is TRUE.
    # This means for very large h, all buildings ARE visible.
    # For h=0, we checked and it might be visible or not.
    # The problem asks for max h where it is NOT possible to see all buildings.
    # So we are looking for the largest h such that is_all_visible(h) is False.
    # Since for large h it is True, and for h=0 it might be False,
    # the function is_all_visible(h) transitions from False to True at some point.
    # We want the largest h where it is False. This is the root of is_all_visible(h) = True/False boundary.
    
    low = 0.0
    high = 2 * 10**9 + 7 # Sufficiently large upper bound
    # Ensure high is a valid "all visible" state
    while not is_all_visible(high):
        high *= 2
        
    # Binary search for the threshold
    # We want max h such that is_all_visible(h) is False.
    # If is_all_visible(mid) is True, then mid is too high (or in the visible region), so answer < mid.
    # If is_all_visible(mid) is False, then mid is in the non-visible region, so answer >= mid.
    
    for _ in range(100):
        mid = (low + high) / 2
        if is_all_visible(mid):
            high = mid
        else:
            low = mid
            
    print(f"{low:.20f}")

solve()