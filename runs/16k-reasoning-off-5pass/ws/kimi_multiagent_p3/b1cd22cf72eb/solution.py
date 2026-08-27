import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    U = [0] * n
    D = [0] * n
    total = 0
    idx = 2
    max_h = 0
    for i in range(n):
        u = int(data[idx]); d = int(data[idx + 1])
        idx += 2
        U[i] = u
        D[i] = d
        total += u + d
        s = u + d
        if s < max_h or max_h == 0:
            pass
    # max feasible H cannot exceed min(U_i + D_i)
    min_sum = min(U[i] + D[i] for i in range(n))

    def feasible(H):
        # u_i in [L_i, R_i]
        # reachable interval propagation
        # initialize with i = 0
        L0 = H - D[0]
        if L0 < 0:
            L0 = 0
        R0 = U[0]
        if R0 > H:
            R0 = H
        if L0 > R0:
            return False
        curL, curR = L0, R0
        for i in range(1, n):
            Li = H - D[i]
            if Li < 0:
                Li = 0
            Ri = U[i]
            if Ri > H:
                Ri = H
            # expand reachable set then intersect
            nL = curL - X
            if nL < Li:
                nL = Li
            nR = curR + X
            if nR > Ri:
                nR = Ri
            if nL > nR:
                return False
            curL, curR = nL, nR
        return True

    lo, hi = 0, min_sum  # hi feasible? not necessarily; binary search max feasible
    # invariant: lo feasible (H=0 always feasible: u_i=d_i=0), find max feasible
    # standard binary search on [0, min_sum]
    ans_h = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            ans_h = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(total - n * ans_h)

main()