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

    # Function to check if all buildings are visible from height h at x=0
    # All buildings are visible iff V_1 < V_2 < ... < V_N
    # where V_k = (H_k - h) / X_k
    def check(h):
        # We need to check if V_0 < V_1 < ... < V_{N-1}
        # To avoid floating point issues with division, we can compare cross-products
        # V_j < V_i  <==> (H_j - h)/X_j < (H_i - h)/X_i
        # Since X_j < X_i (sorted), X_j * X_i > 0.
        # (H_j - h) * X_i < (H_i - h) * X_j
        # H_j * X_i - h * X_i < H_i * X_j - h * X_j
        # H_j * X_i - H_i * X_j < h * (X_i - X_j)
        
        # However, direct floating point comparison is usually stable enough for this problem
        # given the constraints and required precision. Let's use floats.
        
        prev_v = -float('inf')
        for k in range(N):
            # V_k = (H[k] - h) / X[k]
            # Since X[k] >= 1, no division by zero.
            curr_v = (H[k] - h) / X[k]
            if curr_v <= prev_v:
                return False
            prev_v = curr_v
        return True

    # Binary search for the maximum h such that NOT all buildings are visible.
    # If check(h) is True, it means all buildings ARE visible.
    # We want the largest h where check(h) is False.
    # Let's find the boundary.
    # If check(0) is True, then even at h=0 all are visible -> answer -1.
    
    if check(0.0):
        print("-1")
        return

    # Range for binary search
    # Lower bound: 0.0 (we know check(0) is False, so answer >= 0)
    # Upper bound: 10^9 + some margin. Max H is 10^9, max X is 10^9.
    # The intercept can be larger than 10^9?
    # C_{j,i} = (H_j X_i - H_i X_j) / (X_i - X_j).
    # If H_j = 10^9, H_i = 1, X_j = 1, X_i = 10^9.
    # C = (10^9 * 10^9 - 1 * 1) / (10^9 - 1) approx 10^9.
    # So 2*10^9 is a safe upper bound.
    
    low = 0.0
    high = 2.0 * 10**9
    
    # 100 iterations for high precision
    for _ in range(100):
        mid = (low + high) / 2.0
        if check(mid):
            # All visible at mid, so we need higher h to hide something?
            # Wait. If check(mid) is True, all are visible.
            # We want the max h where NOT all are visible.
            # So if all are visible at mid, the answer must be > mid?
            # No. If all are visible at mid, it means mid is "too low" to hide anything?
            # Let's re-evaluate.
            # check(h) returns True if ALL buildings are visible.
            # We want max h such that NOT all buildings are visible.
            # So we want max h such that check(h) is False.
            # If check(mid) is True, then mid is in the "all visible" region.
            # The "all visible" region is [0, h_max_visible).
            # The "not all visible" region is [h_max_visible, infinity).
            # We want the supremum of the "not all visible" region?
            # No, the problem asks for the maximum height at which it is NOT possible to see all buildings.
            # This implies we want the largest h such that check(h) is False.
            # But wait. If h is very large, say h=10^18, then V_k = (H_k - h)/X_k is very negative.
            # V_1 < V_2 < ... < V_N might still hold?
            # Let's check the condition again.
            # V_k = H_k/X_k - h/X_k.
            # As h increases, V_k decreases.
            # The condition V_j < V_i for j < i becomes harder to satisfy as h increases?
            # V_j - V_i = (H_j/X_j - H_i/X_i) - h(1/X_j - 1/X_i).
            # Since X_j < X_i, 1/X_j > 1/X_i, so (1/X_j - 1/X_i) > 0.
            # As h increases, the term -h(...) becomes more negative.
            # So V_j - V_i decreases.
            # If V_j - V_i was positive (V_j > V_i), it might become negative.
            # If V_j - V_i was negative (V_j < V_i), it stays negative.
            # So increasing h makes it MORE LIKELY that V_j < V_i?
            # No. If V_j - V_i decreases, it goes from positive to negative.
            # So V_j < V_i becomes TRUE.
            # So if h is very large, V_j < V_i is likely true for all j < i.
            # This means for very large h, ALL buildings are visible.
            # So check(h) is True for large h.
            # check(0) was False (in our case).
            # So there is a transition from False to True.
            # We want the maximum h such that check(h) is False.
            # This is the boundary point.
            
            # If check(mid) is True, then mid is in the "all visible" region.
            # The answer must be less than mid.
            high = mid
        else:
            # check(mid) is False, meaning not all buildings are visible.
            # This is a candidate for the answer.
            # We can try a larger h.
            low = mid

    print(f"{low:.20f}")

solve()