import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    X = data[1]

    U = [0] * N
    D = [0] * N

    total = 0
    upper = 10**30

    idx = 2
    for i in range(N):
        u = data[idx]
        d = data[idx + 1]
        idx += 2
        U[i] = u
        D[i] = d
        s = u + d
        total += s
        if s < upper:
            upper = s

    def feasible(H):
        # Possible values for the final upper tooth at index 0:
        # max(0, H - D[0]) <= a_0 <= min(U[0], H)
        L = H - D[0]
        if L < 0:
            L = 0
        R = U[0]
        if R > H:
            R = H
        if L > R:
            return False

        lo, hi = L, R

        for i in range(1, N):
            L = H - D[i]
            if L < 0:
                L = 0
            R = U[i]
            if R > H:
                R = H
            if L > R:
                return False

            nlo = lo - X
            if nlo < L:
                nlo = L

            nhi = hi + X
            if nhi > R:
                nhi = R

            if nlo > nhi:
                return False

            lo, hi = nlo, nhi

        return True

    # Maximize the common sum H.
    low, high = 0, upper
    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid - 1

    ans = total - N * low
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    main()