import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    U = [0] * N
    D = [0] * N
    for i in range(N):
        U[i] = int(next(it))
        D[i] = int(next(it))
    
    total = sum(U) + sum(D)  # sum of all original lengths
    # Maximum feasible H is at most the minimum of U_i + D_i
    m = min(U[i] + D[i] for i in range(N))
    lo, hi = 0, m
    best_H = 0
    INF = 10**30
    
    def max_upper_sum(H):
        # Compute L_i, R_i
        L = [0] * N
        R = [0] * N
        for i in range(N):
            R[i] = U[i]
            Li = H - D[i]
            if Li < 0:
                Li = 0
            L[i] = Li
            if L[i] > R[i]:
                return -1  # infeasible for this i
        
        # Forward pass: upper bound from the left
        pref = [0] * N
        cur = INF
        for i in range(N):
            cur = min(cur + X, R[i])
            pref[i] = cur
        # Backward pass: upper bound from the right
        suf = [0] * N
        cur = INF
        for i in range(N - 1, -1, -1):
            cur = min(cur + X, R[i])
            suf[i] = cur
        
        total_up = 0
        for i in range(N):
            ub = min(pref[i], suf[i], R[i])
            if ub < L[i]:
                return -1
            total_up += ub
        return total_up
    
    # Binary search for the maximum feasible H
    while lo <= hi:
        mid = (lo + hi) // 2
        if max_upper_sum(mid) != -1:
            best_H = mid
            lo = mid + 1
        else:
            hi = mid - 1
    
    # Compute answer for the best H
    max_up = max_upper_sum(best_H)
    ans = total - N * best_H - max_up
    print(ans)

if __name__ == "__main__":
    solve()