import random
import bisect

def brute_force(A, L, R):
    # Exhaustive search for maximum matching in [L,R]
    # Each mochi can be top or bottom. We need max pairs (t,b) with t != b,
    # A[t] <= A[b]/2. This is a bipartite matching problem on a small set.
    # We can use DP over subsets since size <= 15 for brute force.
    n = R - L + 1
    if n <= 1:
        return 0
    # Indices in original array
    idx = list(range(L, R+1))
    # Build compatibility: can i be top with j as bottom?
    compat = [[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j: continue
            if A[idx[i]] * 2 <= A[idx[j]]:
                compat[i][j] = True
    # Maximum matching in bipartite graph (tops vs bottoms, but both are the same set)
    # Since each mochi can be used once, this is a general matching problem.
    # We can use DP on subsets: match the first unused mochi as either bottom or top.
    # But simpler: try all pairings? n <= 10 for brute force.
    from functools import lru_cache
    # State: tuple of available indices. We pair them greedily? Let's do recursion.
    def solve(available):
        if not available:
            return 0
        # pick the smallest index in available
        i = min(available)
        best = 0
        # Option 1: i is a bottom (unmatched)
        best = max(best, solve(available - {i}))
        # Option 2: i is a top, match with some j
        for j in available:
            if j == i: continue
            if compat[i - L][j - L]:  # careful with index shift
                new_avail = available - {i, j}
                best = max(best, 1 + solve(new_avail))
        return best
    initial = frozenset(idx)
    return solve(initial)

def precompute_next(A):
    N = len(A)
    nxt = [N+1] * N
    j = N
    for i in range(N-1, -1, -1):
        while j > i and A[j] >= 2 * A[i]:
            j -= 1
        # After loop, A[j] < 2*A[i] or j == i. We need first index > i with A[idx] >= 2*A[i].
        # Actually we want smallest idx > i with A[idx] >= 2*A[i]. 
        # The two-pointer: we maintain j as the first index such that A[j] >= 2*A[i]? Let's do carefully.
        pass
    # Better two-pointer:
    nxt = [N+1] * N
    j = N
    for i in range(N-1, -1, -1):
        # We need smallest k > i with A[k] >= 2*A[i]
        # We can move j leftwards while j > i and A[j] < 2*A[i]? No, j is currently the first valid? 
        # Standard: for each i from N-1 downto 0, find first j > i with A[j] >= 2*A[i].
        # We can do:
        while j > i and A[j] >= 2 * A[i]:
            j -= 1
        # After loop, either j == i or A[j] < 2*A[i]. The first valid is j+1 if j+1 <= N-1.
        # But we need j > i. So if A[j] >= 2*A[i] for some j > i, we want the smallest such.
        # The loop above stops when A[j] < 2*A[i] or j == i. So j+1 is the first valid.
        if j + 1 < N and j + 1 > i:
            nxt[i] = j + 1
        else:
            nxt[i] = N + 1
    return nxt

def greedy_two_pointer(A, nxt, L, R):
    # Compute answer using the two-pointer greedy
    # M = last index with nxt[M] <= R
    N = len(A)
    # Find M in [L,R]: actually M depends on R, could be < L.
    # We need T = min(R, M)
    # Find M: binary search for largest i in [0,N-1] with nxt[i] <= R.
    lo, hi = 0, N-1
    M = -1
    while lo <= hi:
        mid = (lo+hi)//2
        if nxt[mid] <= R:
            M = mid
            lo = mid + 1
        else:
            hi = mid - 1
    if M < L:
        return 0
    T = min(R, M)
    K = T - L + 1
    p = L
    ans = 0
    for i in range(L, T+1):
        # advance p until p >= nxt[i] or p > R
        if p < nxt[i]:
            p = nxt[i]
        if p > R:
            break
        # match i with p
        ans += 1
        p += 1
    return ans

def test_random():
    for N in range(2, 12):
        for _ in range(100):
            A = sorted(random.randint(1, 20) for _ in range(N))
            nxt = precompute_next(A)
            # Test all queries
            for L in range(1, N+1):
                for R in range(L+1, N+1):
                    bf = brute_force(A, L, R)
                    gr = greedy_two_pointer(A, nxt, L-1, R-1)  # convert to 0-indexed
                    if bf != gr:
                        print(f"Mismatch! N={N}, A={A}, L={L}, R={R}")
                        print(f"  next: {nxt}")
                        print(f"  brute: {bf}, greedy: {gr}")
                        return
    print("All tests passed!")

if __name__ == "__main__":
    test_random()