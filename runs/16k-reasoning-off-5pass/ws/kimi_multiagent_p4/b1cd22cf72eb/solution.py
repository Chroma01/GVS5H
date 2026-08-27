import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); X = int(data[1])
    U = [0]*n
    D = [0]*n
    idx = 2
    S = 0
    for i in range(n):
        u = int(data[idx]); d = int(data[idx+1]); idx += 2
        U[i] = u; D[i] = d
        S += u + d

    def feasible(H):
        # For fixed H: final upper u_i must satisfy max(0, H-D_i) <= u_i <= min(U_i, H)
        # and be X-Lipschitz. The feasible set is closed under componentwise max,
        # so compute the greatest element g = min_j(R_j + X|i-j|) via forward/backward
        # passes; H is feasible iff g_i >= H - D_i for all i.
        g = [0]*n
        prev = U[0] if U[0] < H else H
        g[0] = prev
        for i in range(1, n):
            r = U[i] if U[i] < H else H
            v = prev + X
            if r < v:
                v = r
            g[i] = v
            prev = v
        l = H - D[n-1]
        if l > 0 and g[n-1] < l:
            return False
        nxt = g[n-1]
        for i in range(n-2, -1, -1):
            v = nxt + X
            if g[i] > v:
                g[i] = v
            l = H - D[i]
            if l > 0 and g[i] < l:
                return False
            nxt = g[i]
        return True

    lo = 0
    hi = 2_000_000_000  # H <= max(U_i + D_i) <= 2e9
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    # cost = sum(U_i - g_i) + sum(D_i - (H - g_i)) = S - N*H
    print(S - n * lo)

main()