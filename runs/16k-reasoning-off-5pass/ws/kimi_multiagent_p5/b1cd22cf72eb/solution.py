import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    U = [0] * N
    D = [0] * N
    total = 0
    min_sum = None
    for i in range(N):
        u = int(data[idx]); idx += 1
        d = int(data[idx]); idx += 1
        U[i] = u
        D[i] = d
        s = u + d
        total += s
        if min_sum is None or s < min_sum:
            min_sum = s

    def feasible(H):
        # u_i in [max(0, H - D_i), min(U_i, H)]
        # forward reachable interval
        lo = H - D[0]
        if lo < 0:
            lo = 0
        hi = U[0] if U[0] < H else H
        if lo > hi:
            return False
        for i in range(1, N):
            L = H - D[i]
            if L < 0:
                L = 0
            R = U[i] if U[i] < H else H
            # intersect with [lo - X, hi + X]
            nlo = lo - X
            if L > nlo:
                nlo = L
            nhi = hi + X
            if R < nhi:
                nhi = R
            if nlo > nhi:
                return False
            lo = nlo
            hi = nhi
        return True

    lo_h = 0
    hi_h = min_sum  # H <= min(U_i + D_i)
    # binary search max feasible H in [lo_h, hi_h]
    while lo_h < hi_h:
        mid = (lo_h + hi_h + 1) // 2
        if feasible(mid):
            lo_h = mid
        else:
            hi_h = mid - 1

    print(total - N * lo_h)

main()