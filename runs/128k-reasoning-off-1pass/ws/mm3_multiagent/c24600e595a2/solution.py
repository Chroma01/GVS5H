import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    C = [int(next(it)) for _ in range(N)]
    
    # initial total sum S = sum A_k * C_k
    S = 0
    mismatches = []  # list of (C_i, B_i) for indices where A_i != B_i
    for i in range(N):
        S += A[i] * C[i]
        if A[i] != B[i]:
            mismatches.append((C[i], B[i]))
    
    # process mismatches in increasing C
    mismatches.sort(key=lambda x: x[0])
    
    total_cost = 0
    for c, b in mismatches:
        total_cost += S
        # after flipping, A_i becomes b, so contribution changes by (b - original_A_i) * c
        # original_A_i is 1-A[i]?? Wait we stored B_i. We need original A_i.
        # We'll re-derive: we have A_i and B_i from the original arrays.
        # Since we are iterating mismatches, we need to know the original A_i.
        # Let's store (C_i, B_i, A_i) instead.
        pass