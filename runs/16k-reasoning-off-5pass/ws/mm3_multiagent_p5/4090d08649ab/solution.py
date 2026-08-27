import sys
from collections import defaultdict

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    total = N * (N + 1) // 2
    
    # Build positions for each value (1-indexed values up to N)
    pos = [[] for _ in range(N + 2)]
    for idx, v in enumerate(A, start=1):
        pos[v].append(idx)
    
    # Compute missing for each value
    missing = [0] * (N + 2)
    for v in range(1, N + 1):
        p = pos[v]
        prev = 0
        m = 0
        for x in p:
            gap = x - prev - 1
            m += gap * (gap + 1) // 2  # wait, binom(gap, 2)? No, we need binom(len, 2).
            # Let's use: subarrays in a gap of length L (number of positions strictly between prev and x) is C(L, 2).
            # Actually, if gap = x - prev - 1, then the number of subarrays completely inside this gap is gap * (gap + 1) // 2? No.
            # The subarrays that miss v are those entirely within the gap. The gap has length (x - prev - 1) positions (indices from prev+1 to x-1).
            # Number of subarrays in a segment of length L is L*(L+1)//2. That's for any subarray.
            # Wait, we want subarrays that contain no occurrence of v. The gap between occurrences (including before first and after last) is a maximal interval without v.
            # The length of the gap is (next - prev - 1) positions. The number of subarrays within that gap is binom(L+1, 2)? No, standard formula: number of subarrays in a contiguous block of length L is L*(L+1)//2.
            # So if the gap has L = x - prev - 1 positions, then number of subarrays missing v in that gap is L*(L+1)//2.
            # Let's verify: N=4, A=[1,3,1,4]. v=1, pos=[1,3]. prev=0, x=1, L=0 -> 0. prev=1, x=3, L=1 -> 1*(2)/2=1. prev=3, final N+1=5, L=5-3-1=1 -> 1. Total missing=2. Correct.
            # So formula: missing += L*(L+1)//2
            prev = x
        # final gap
        gap = N + 1 - prev - 1  # wait, N+1 - prev - 1 = N - prev
        L = N - prev
        m += L * (L + 1) // 2
        missing[v] = m
    
    # Compute Sum_D
    Sum_D = 0
    for v in range(1, N + 1):
        Sum_D += total - missing[v]
    
    # Compute Sum_G
    Sum_G = 0
    for x in range(1, N):
        X = pos[x]
        Y = pos[x + 1]
        if not X or not Y:
            continue
        # Merge to find missing both
        i, j = 0, 0
        prev = 0
        missing_both = 0
        lenX, lenY = len(X), len(Y)
        while i < lenX and j < lenY:
            if X[i] < Y[j]:
                curr = X[i]; i += 1
            else:
                curr = Y[j]; j += 1
            L = curr - prev - 1
            missing_both += L * (L + 1) // 2
            prev = curr
        while i < lenX:
            curr = X[i]; i += 1
            L = curr - prev - 1
            missing_both += L * (L + 1) // 2
            prev = curr
        while j < lenY:
            curr = Y[j]; j += 1
            L = curr - prev - 1
            missing_both += L * (L + 1) // 2
            prev = curr
        L = N - prev
        missing_both += L * (L + 1) // 2
        
        G = total - missing[x] - missing[x + 1] + missing_both
        Sum_G += G
    
    print(Sum_D - Sum_G)

if __name__ == "__main__":
    solve()