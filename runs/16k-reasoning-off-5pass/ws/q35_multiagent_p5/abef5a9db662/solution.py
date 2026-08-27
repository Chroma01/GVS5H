import sys

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(2000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    contests = []
    max_L = 0
    max_R = 0
    
    for _ in range(N):
        L = int(next(iterator))
        R = int(next(iterator))
        contests.append((L, R))
        if L > max_L: max_L = L
        if R > max_R: max_R = R

    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    queries = []
    for _ in range(Q):
        queries.append(int(next(iterator)))

    # Max initial rating is 500,000
    MAX_X = 500000
    
    # We need to support:
    # 1. Point query: get h(X) = X + diff(X)
    # 2. Range update: add v to diff[l...r]
    # We use a Fenwick Tree (BIT) for range updates and point queries.
    # Standard BIT supports point update and prefix sum.
    # To support range update [l, r] with val and point query at i:
    # We use a BIT on the difference array D.
    # Update(l, r, val): add val to D[l], subtract val from D[r+1]
    # Query(i): prefix sum of D up to i gives the total added to index i.
    
    size = MAX_X + 2
    bit = [0] * (size + 1)
    
    def bit_add(idx, val):
        """Add val to element at idx (1-based)"""
        while idx <= size:
            bit[idx] += val
            idx += idx & (-idx)
            
    def bit_query(idx):
        """Return prefix sum up to idx (1-based)"""
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s

    # Initial state: h(X) = X. So diff(X) = 0 for all X.
    # BIT is already all zeros.
    
    # Helper to get current h(X)
    def get_h(X):
        return X + bit_query(X)

    # Binary search for smallest X in [1, MAX_X] such that h(X) >= target
    def find_left(target):
        low = 1
        high = MAX_X
        ans = MAX_X + 1 # Not found
        
        while low <= high:
            mid = (low + high) // 2
            if get_h(mid) >= target:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans

    # Binary search for largest X in [1, MAX_X] such that h(X) <= target
    def find_right(target):
        low = 1
        high = MAX_X
        ans = 0 # Not found
        
        while low <= high:
            mid = (low + high) // 2
            if get_h(mid) <= target:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        return ans

    # Process each contest
    for L, R in contests:
        # Find range [A, B] of starting ratings X such that current h(X) is in [L, R]
        A = find_left(L)
        B = find_right(R)
        
        if A <= B and A <= MAX_X and B >= 1:
            # Clamp to valid range [1, MAX_X]
            A = max(1, A)
            B = min(MAX_X, B)
            
            if A <= B:
                # Range add 1 to diff[A...B]
                # Update BIT: add 1 at A, subtract 1 at B+1
                bit_add(A, 1)
                if B + 1 <= size:
                    bit_add(B + 1, -1)

    # Answer queries
    results = []
    for X in queries:
        # X is guaranteed to be in [1, 500000]
        final_rating = X + bit_query(X)
        results.append(str(final_rating))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()