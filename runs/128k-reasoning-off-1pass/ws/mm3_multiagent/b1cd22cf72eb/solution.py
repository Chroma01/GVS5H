import sys

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    X = int(input_data[idx]); idx += 1
    U = []
    D = []
    S = []
    total = 0
    minS = 10**19
    for _ in range(N):
        u = int(input_data[idx]); idx += 1
        d = int(input_data[idx]); idx += 1
        U.append(u)
        D.append(d)
        s = u + d
        S.append(s)
        total += s
        if s < minS:
            minS = s

    # Feasibility check for a given H
    def feasible(H):
        # large bounds to simulate infinity
        low = -10**19
        high = 10**19
        for i in range(N):
            # L_i = max(0, H - D[i])
            L = H - D[i]
            if L < 0:
                L = 0
            # R_i = min(U[i], H)
            R = U[i]
            if R > H:
                R = H
            if L > R:
                return False
            # apply Lipschitz constraint
            low = max(L, low - X)
            high = min(R, high + X)
            if low > high:
                return False
        return True

    # Binary search for maximum feasible H in [0, minS]
    lo = 0
    hi = minS
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    ans = total - N * lo
    print(ans)

if __name__ == "__main__":
    solve()