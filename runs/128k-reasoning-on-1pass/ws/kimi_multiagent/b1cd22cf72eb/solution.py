import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = int(data[1])
    U = [0] * n
    D = [0] * n
    idx = 2
    total = 0
    min_sum = None
    for i in range(n):
        u = int(data[idx]); d = int(data[idx + 1])
        idx += 2
        U[i] = u
        D[i] = d
        s = u + d
        total += s
        if min_sum is None or s < min_sum:
            min_sum = s

    def feasible(H, U=U, D=D, X=X, n=n):
        # allowed upper length at position i: [max(0, H-D[i]), min(U[i], H)]
        lo = H - D[0]
        if lo < 0:
            lo = 0
        hi = U[0]
        if hi > H:
            hi = H
        if lo > hi:
            return False
        for i in range(1, n):
            nlo = H - D[i]
            if nlo < 0:
                nlo = 0
            nhi = U[i]
            if nhi > H:
                nhi = H
            # intersect with reachable [lo - X, hi + X]
            a = lo - X
            if nlo < a:
                nlo = a
            b = hi + X
            if nhi > b:
                nhi = b
            if nlo > nhi:
                return False
            lo = nlo
            hi = nhi
        return True

    lo_h = 0
    hi_h = min_sum
    while lo_h < hi_h:
        mid = (lo_h + hi_h + 1) // 2
        if feasible(mid):
            lo_h = mid
        else:
            hi_h = mid - 1

    print(total - n * lo_h)

main()