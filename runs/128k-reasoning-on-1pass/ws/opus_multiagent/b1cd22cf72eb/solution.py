import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); X = int(data[1])
    try:
        import numpy as np
    except Exception:
        np = None

    if np is not None:
        arr = np.array(data[2:2 + 2 * n], dtype=np.int64)
        U = arr[0::2].copy()
        D = arr[1::2].copy()
        S = int((U + D).sum())
        Xi = X * np.arange(n, dtype=np.int64)
        hiU = int((U + D).min())

        def feasible(H):
            lo = H - D
            np.maximum(lo, 0, out=lo)
            hi = np.minimum(U, H)
            if (lo > hi).any():
                return False
            a = lo + Xi
            b = hi + Xi
            np.maximum.accumulate(a, out=a)
            if (a > b).any():
                return False
            c = lo - Xi
            d = hi - Xi
            c = c[::-1].copy()
            np.maximum.accumulate(c, out=c)
            c = c[::-1]
            if (c > d).any():
                return False
            return True

        loH, hiH = 0, hiU
        # H = 0 always feasible
        while loH < hiH:
            mid = (loH + hiH + 1) // 2
            if feasible(mid):
                loH = mid
            else:
                hiH = mid - 1
        sys.stdout.write(str(int(S - n * loH)) + "\n")
        return

    # Pure-python fallback
    vals = list(map(int, data[2:2 + 2 * n]))
    U = vals[0::2]
    D = vals[1::2]
    S = sum(U) + sum(D)
    hiU = min(U[i] + D[i] for i in range(n))

    def feasible_py(H):
        l = H - D[0]
        if l < 0:
            l = 0
        r = U[0]
        if H < r:
            r = H
        if l > r:
            return False
        for i in range(1, n):
            li = H - D[i]
            if li < 0:
                li = 0
            ri = U[i]
            if H < ri:
                ri = H
            nl = l - X
            if li > nl:
                nl = li
            nr = r + X
            if ri < nr:
                nr = ri
            if nl > nr:
                return False
            l = nl
            r = nr
        return True

    loH, hiH = 0, hiU
    while loH < hiH:
        mid = (loH + hiH + 1) // 2
        if feasible_py(mid):
            loH = mid
        else:
            hiH = mid - 1
    sys.stdout.write(str(S - n * loH) + "\n")


main()