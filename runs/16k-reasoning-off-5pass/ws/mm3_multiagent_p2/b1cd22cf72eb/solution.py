import sys

def solve():
    input_data = sys.stdin.read().split()
    it = iter(input_data)
    N = int(next(it))
    X = int(next(it))
    U = []
    D = []
    S = []
    maxS = 0
    sumS = 0
    for _ in range(N):
        u = int(next(it))
        d = int(next(it))
        U.append(u)
        D.append(d)
        s = u + d
        S.append(s)
        if s > maxS:
            maxS = s
        sumS += s
    # feasibility check for a given H
    def feasible(H):
        lo = max(0, H - D[0])
        hi = min(U[0], H)
        if lo > hi:
            return False
        for i in range(1, N):
            Li = max(0, H - D[i])
            Ri = min(U[i], H)
            if Li > Ri:
                return False
            lo = max(Li, lo - X)
            hi = min(Ri, hi + X)
            if lo > hi:
                return False
        return True
    # binary search maximum H
    loH = 0
    hiH = maxS
    # while loH < hiH, find highest feasible
    while loH < hiH:
        mid = (loH + hiH + 1) // 2
        if feasible(mid):
            loH = mid
        else:
            hiH = mid - 1
    H_opt = loH
    ans = sumS - N * H_opt
    print(ans)

if __name__ == "__main__":
    solve()