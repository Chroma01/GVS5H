import sys

def solve():
    import sys
    input = sys.stdin.readline
    N_X = input().split()
    while len(N_X) < 2:
        N_X += input().split()
    N = int(N_X[0])
    X = int(N_X[1])
    U = [0] * N
    D = [0] * N
    total = 0
    min_sum = None
    for i in range(N):
        line = input().split()
        while len(line) < 2:
            line += input().split()
        u = int(line[0])
        d = int(line[1])
        U[i] = u
        D[i] = d
        total += u + d
        s = u + d
        if min_sum is None or s < min_sum:
            min_sum = s

    # Feasibility check for a given H
    def can(H):
        lo = max(0, H - D[0])
        hi = U[0]
        if lo > hi:
            return False
        for i in range(1, N):
            low_i = H - D[i]
            if low_i < 0:
                low_i = 0
            high_i = U[i]
            new_lo = max(low_i, lo - X)
            new_hi = min(high_i, hi + X)
            if new_lo > new_hi:
                return False
            lo, hi = new_lo, new_hi
        return True

    # Binary search maximum feasible H in [0, min_sum]
    lo_H, hi_H = 0, min_sum
    best = 0
    # We can use standard binary search; H is integer.
    while lo_H <= hi_H:
        mid = (lo_H + hi_H) // 2
        if can(mid):
            best = mid
            lo_H = mid + 1
        else:
            hi_H = mid - 1

    ans = total - N * best
    print(ans)

if __name__ == "__main__":
    solve()