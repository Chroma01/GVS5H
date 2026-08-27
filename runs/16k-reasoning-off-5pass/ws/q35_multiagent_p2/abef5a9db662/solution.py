import sys

def solve():
    # Increase recursion depth just in case, though we won't use recursion
    sys.setrecursionlimit(2000)
    
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    contests = []
    for _ in range(N):
        L = int(next(iterator))
        R = int(next(iterator))
        contests.append((L, R))
        
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    queries = []
    for _ in range(Q):
        queries.append(int(next(iterator)))
        
    # Max initial rating is 500,000.
    # Max possible rating is 500,000 + 200,000 = 700,000.
    # We need to track S[X] for X in [1, 500000].
    # S[X] is the number of contests that triggered for initial rating X.
    # We use a Fenwick tree (BIT) to maintain the difference array D_S.
    # S[X] = prefix_sum(D_S, X).
    # Range update [l, r] on S corresponds to:
    # D_S[l] += 1, D_S[r+1] -= 1.
    # Point query S[X] is prefix_sum(D_S, X).
    
    MAX_X = 500005
    # BIT array, 1-indexed
    bit = [0] * (MAX_X + 2)
    
    def bit_update(idx, val):
        """Add val to element at idx (1-indexed)"""
        while idx < MAX_X + 2:
            bit[idx] += val
            idx += idx & (-idx)
            
    def bit_query(idx):
        """Return prefix sum up to idx (1-indexed)"""
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s

    # For each contest, we need to find the range [X_min, X_max] of initial ratings X
    # such that the current rating at this contest is in [L, R].
    # Current rating for initial X is: r(X) = X + S[X] = X + bit_query(X).
    # We need L <= X + bit_query(X) <= R.
    # Since X + bit_query(X) is strictly increasing with X (because bit_query(X) is non-decreasing),
    # we can binary search for X_min and X_max.
    
    # Helper function to compute current rating for initial X
    def current_rating(X):
        if X < 1:
            return 0 # Should not happen for valid X
        if X > 500000:
            # For X > 500000, S[X] is 0 because we only update up to 500000
            # Actually, we only care about X in [1, 500000] for queries.
            # But binary search might probe outside.
            # If X > 500000, S[X] = 0.
            return X
        return X + bit_query(X)

    # Binary search for the smallest X such that current_rating(X) >= L
    def find_min_X(L):
        low = 1
        high = 500000
        ans = -1
        while low <= high:
            mid = (low + high) // 2
            if current_rating(mid) >= L:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans

    # Binary search for the largest X such that current_rating(X) <= R
    def find_max_X(R):
        low = 1
        high = 500000
        ans = -1
        while low <= high:
            mid = (low + high) // 2
            if current_rating(mid) <= R:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        return ans

    for L, R in contests:
        # Find the range of initial X that trigger this contest
        X_min = find_min_X(L)
        X_max = find_max_X(R)
        
        if X_min != -1 and X_max != -1 and X_min <= X_max:
            # Update the difference array for S: add 1 to S[X] for X in [X_min, X_max]
            # This is done by updating BIT at X_min with +1 and at X_max+1 with -1
            bit_update(X_min, 1)
            if X_max + 1 < MAX_X + 2:
                bit_update(X_max + 1, -1)
                
    # Now compute the final answers for all X in [1, 500000]
    # S[X] is bit_query(X)
    # Final rating for initial X is X + S[X]
    
    # Precompute answers for all X in [1, 500000]
    ans_for_x = [0] * (MAX_X + 1)
    for x in range(1, 500001):
        s_x = bit_query(x)
        ans_for_x[x] = x + s_x
        
    # Process queries
    results = []
    for q in queries:
        if q < 1:
            # If query is less than 1, it's outside our precomputed range.
            # However, constraints say 1 <= X <= 500000.
            # Just in case, handle it.
            # For X < 1, S[X] = 0, so answer is X.
            results.append(str(q))
        elif q > 500000:
            # For X > 500000, S[X] = 0, so answer is X.
            results.append(str(q))
        else:
            results.append(str(ans_for_x[q]))
            
    print('\n'.join(results))

solve()