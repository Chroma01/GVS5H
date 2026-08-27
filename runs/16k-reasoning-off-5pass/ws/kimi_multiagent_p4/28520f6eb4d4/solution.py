import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    X = [0] * n
    H = [0] * n
    idx = 1
    for i in range(n):
        X[i] = int(data[idx]); H[i] = int(data[idx + 1])
        idx += 2

    if n == 1:
        sys.stdout.write("-1\n")
        return

    # Upper convex hull of points (X_j, H_j) seen so far.
    # Slopes between consecutive hull vertices are strictly decreasing.
    hx = [X[0]]
    hh = [H[0]]

    # Best (maximum) candidate intercept, kept as exact rational num/den (den > 0).
    best_num = None
    best_den = 1

    def consider(num, den):
        # candidate intercept = num / den
        nonlocal best_num, best_den
        if den < 0:
            num = -num
            den = -den
        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

    for i in range(1, n):
        xi = X[i]
        hi = H[i]

        # ---- Tangent query: find hull vertex j maximizing the y-intercept at x=0
        # of the line through (hx[j], hh[j]) and (xi, hi).
        # intercept(j) = (hh[j]*xi - hi*hx[j]) / (xi - hx[j]), denominator > 0.
        # This is unimodal along the hull: binary search comparing neighbors.
        lo = 0
        hi_h = len(hx) - 1
        while lo < hi_h:
            mid = (lo + hi_h) // 2
            x1 = hx[mid];     h1 = hh[mid]
            x2 = hx[mid + 1]; h2 = hh[mid + 1]
            # i1 = (h1*xi - hi*x1)/(xi - x1), i2 = (h2*xi - hi*x2)/(xi - x2)
            n1 = h1 * xi - hi * x1
            d1 = xi - x1
            n2 = h2 * xi - hi * x2
            d2 = xi - x2
            # if i2 >= i1 move right
            if n2 * d1 >= n1 * d2:
                lo = mid + 1
            else:
                hi_h = mid
        j = lo
        num = hh[j] * xi - hi * hx[j]
        den = xi - hx[j]
        consider(num, den)

        # ---- Insert (xi, hi) into upper hull.
        while len(hx) >= 2:
            x1 = hx[-2]; h1 = hh[-2]
            x2 = hx[-1]; h2 = hh[-1]
            cross = (x2 - x1) * (hi - h1) - (h2 - h1) * (xi - x1)
            if cross >= 0:
                hx.pop()
                hh.pop()
            else:
                break
        hx.append(xi)
        hh.append(hi)

    if best_num is None or best_num < 0:
        sys.stdout.write("-1\n")
    else:
        ans = best_num / best_den
        sys.stdout.write("{:.18f}\n".format(ans))

solve()