import sys

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    X = data[1]

    U = [0] * N
    D = [0] * N

    total_s = 0
    min_s = 10**30
    idx = 2
    for i in range(N):
        u = data[idx]
        d = data[idx + 1]
        idx += 2
        U[i] = u
        D[i] = d
        s = u + d
        total_s += s
        if s < min_s:
            min_s = s

    def feasible(H: int) -> bool:
        # interval of possible upper lengths at position 0
        lo = H - D[0]
        if lo < 0:
            lo = 0
        hi = U[0]
        if H < hi:
            hi = H

        for i in range(1, N):
            L = H - D[i]
            if L < 0:
                L = 0
            R = U[i]
            if H < R:
                R = H

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

    low = 0
    high = min_s
    ans = 0

    while low <= high:
        mid = (low + high) // 2
        if feasible(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1

    print(total_s - N * ans)

if __name__ == "__main__":
    solve()