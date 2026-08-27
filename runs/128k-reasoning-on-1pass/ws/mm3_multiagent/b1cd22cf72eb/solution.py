import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    X = int(next(it))

    U = [0] * N
    D = [0] * N
    totalS = 0
    minS = 10 ** 30          # larger than any possible sum

    for i in range(N):
        u = int(next(it))
        d = int(next(it))
        U[i] = u
        D[i] = d
        s = u + d
        totalS += s
        if s < minS:
            minS = s

    # ------------------------------------------------------------
    # Feasibility test: does there exist a sequence of U'[i] satisfying
    #   U'[i] in [max(0, H-D[i]), min(U[i], H)]
    #   |U'[i] - U'[i+1]| ≤ X
    def feasible(H: int) -> bool:
        # reachable interval for the previous position (very large bounds)
        L = -10 ** 30
        R = 10 ** 30
        x = X
        for i in range(N):
            # own interval for this position
            low = H - D[i]
            if low < 0:
                low = 0
            up = U[i]
            if up > H:
                up = H

            # intersect with shifted previous interval
            # new L = max(low, L - X)
            L = low if low > L - x else L - x
            # new R = min(up,  R + X)
            R = up  if up  < R + x else R + x
            if L > R:
                return False
        return True
    # ------------------------------------------------------------

    lo, hi = 0, minS
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    Hmax = lo
    answer = totalS - N * Hmax
    print(answer)


if __name__ == "__main__":
    solve()