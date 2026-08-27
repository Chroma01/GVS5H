import sys
from collections import Counter

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    
    # Count -1 placeholders
    cntA1 = A.count(-1)
    cntB1 = B.count(-1)
    if cntA1 != cntB1:
        print("No")
        return
    
    fixed_A = [x for x in A if x != -1]
    fixed_B = [x for x in B if x != -1]
    nA = len(fixed_A)
    nB = len(fixed_B)
    
    # Check consistency of fixed pairs (both A_i and B_i are not -1)
    S_fixed = None
    conflict = False
    for i in range(N):
        if A[i] != -1 and B[i] != -1:
            s = A[i] + B[i]
            if S_fixed is None:
                S_fixed = s
            elif s != S_fixed:
                conflict = True
                break
    if conflict:
        print("No")
        return
    
    max_A = max(fixed_A) if fixed_A else 0
    max_B = max(fixed_B) if fixed_B else 0
    M = max(max_A, max_B)
    
    # T = nA + nB - N (minimum number of required fixed-fixed matches)
    T = nA + nB - N
    
    # If S is fixed, we must use that S
    if S_fixed is not None:
        if S_fixed < M:
            print("No")
            return
        # Compute k(S_fixed)
        k = compute_k(fixed_A, fixed_B, S_fixed)
        if k >= T:
            print("Yes")
        else:
            print("No")
        return
    
    # S is not fixed
    if T <= 0:
        # Flexible slots are enough, choose S = M
        print("Yes")
        return
    
    # T > 0: need to find S >= M with k(S) >= T
    # Build frequency maps
    cntA = Counter(fixed_A)
    cntB = Counter(fixed_B)
    distinct_A = list(cntA.keys())
    distinct_B = list(cntB.keys())
    
    # Efficiently compute k(S) for all candidate S = a + b
    k_map = {}
    for a in distinct_A:
        ca = cntA[a]
        for b in distinct_B:
            cb = cntB[b]
            S = a + b
            contribution = min(ca, cb)
            if contribution > 0:
                k_map[S] = k_map.get(S, 0) + contribution
    
    # Check candidates S >= M
    for S, k in k_map.items():
        if S >= M and k >= T:
            print("Yes")
            return
    
    print("No")

def compute_k(fixed_A, fixed_B, S):
    """Compute maximum matching count for a given S."""
    cntA = Counter(fixed_A)
    cntB = Counter(fixed_B)
    k = 0
    for a, ca in cntA.items():
        b = S - a
        if b in cntB:
            k += min(ca, cntB[b])
    return k

if __name__ == "__main__":
    solve()