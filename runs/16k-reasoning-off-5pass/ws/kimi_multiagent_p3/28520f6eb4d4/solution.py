import sys

def solve():
    data = sys.stdin.buffer.read().split()
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

    # Upper hull of points (X_j, H_j), X strictly increasing.
    # Consecutive slopes strictly decreasing.
    hx = [X[0]]
    hh = [H[0]]

    M = None  # maximum intercept found

    for i in range(1, n):
        xp = X[i]; hp = H[i]

        # Binary search hull vertex minimizing slope to (xp, hp).
        # slope(a, P) = (hp - ha) / (xp - xa), denominators positive.
        lo = 0
        hi = len(hx) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            # compare f(mid) vs f(mid+1)
            # f(k) = (hp - hh[k]) / (xp - hx[k])
            lhs = (hp - hh[mid]) * (xp - hx[mid + 1])
            rhs = (hp - hh[mid + 1]) * (xp - hx[mid])
            if lhs < rhs:
                hi = mid          # f(mid) < f(mid+1): minimum in [lo, mid]
            else:
                lo = mid + 1      # minimum in [mid+1, hi]
        j = lo
        # intercept b = (H_j * X_i - H_i * X_j) / (X_i - X_j)
        num = hh[j] * xp - hp * hx[j]
        den = xp - hx[j]
        b = num / den
        if M is None or b > M:
            M = b

        # Insert (xp, hp) into upper hull.
        # Pop while slope(hull[-2], hull[-1]) <= slope(hull[-1], new)
        while len(hx) >= 2:
            x1, y1 = hx[-2], hh[-2]
            x2, y2 = hx[-1], hh[-1]
            # (y2 - y1)/(x2 - x1) <= (hp - y2)/(xp - x2) ?
            if (y2 - y1) * (xp - x2) <= (hp - y2) * (x2 - x1):
                hx.pop(); hh.pop()
            else:
                break
        hx.append(xp); hh.append(hp)

    if M is None or M < 0:
        sys.stdout.write("-1\n")
    else:
        sys.stdout.write("{:.15f}\n".format(M))

solve()