import sys

def main():
    input = sys.stdin.readline
    N, X = map(int, input().split())
    U = [0] * N
    D = [0] * N
    S = [0] * N
    total = 0
    max_sum = 0
    for i in range(N):
        u, d = map(int, input().split())
        U[i] = u
        D[i] = d
        S[i] = u + d
        total += S[i]
        if S[i] > max_sum:
            max_sum = S[i]

    def check(H):
        # u_i in [L_i, R_i] with |u_i - u_{i+1}| <= X
        # L_i = max(0, H - D_i), R_i = min(U_i, H)
        # Forward pass: propagate reachable lower bounds
        # low[i] = max(L_i, low[i-1] - X)
        # high[i] = min(R_i, high[i-1] + X)
        # Then check low[i] <= high[i] for all i
        # Actually, a single forward pass with both bounds is sufficient
        # because constraints are symmetric: feasible iff after forward
        # propagation low[i] <= high[i] for all i.
        low = max(0, H - D[0])
        high = min(U[0], H)
        if low > high:
            return False
        for i in range(1, N):
            L = H - D[i]
            if L < 0:
                L = 0
            R = U[i]
            if R > H:
                R = H
            low = low - X
            if low < L:
                low = L
            high = high + X
            if high > R:
                high = R
            if low > high:
                return False
        return True

    lo, hi = 0, max_sum
    # find max feasible H
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if check(mid):
            lo = mid
        else:
            hi = mid - 1

    print(total - N * lo)

main()