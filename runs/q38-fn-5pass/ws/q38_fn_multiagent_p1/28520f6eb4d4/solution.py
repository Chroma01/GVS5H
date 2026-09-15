import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]

    # Upper hull of previous building tops.
    xs = []
    hs = []

    # Edge differences of the hull:
    # edx[k] = xs[k+1] - xs[k], edy[k] = hs[k+1] - hs[k]
    edx = []
    edy = []

    # Best threshold as an exact rational best_num / best_den.
    best_num = None
    best_den = 1

    p = 1
    for _ in range(n):
        x = data[p]
        h = data[p + 1]
        p += 2

        m = len(xs)

        # Query the previous upper hull for the vertex minimizing slope to (x, h).
        if m:
            lo = 0
            hi = m - 1

            # Predicate:
            # slope(P[mid], C) <= slope(P[mid+1], C)
            # is equivalent to edge_slope(mid) <= slope(P[mid+1], C).
            while lo < hi:
                mid = (lo + hi) >> 1
                mid1 = mid + 1

                if edy[mid] * (x - xs[mid1]) <= (h - hs[mid1]) * edx[mid]:
                    hi = mid
                else:
                    lo = mid + 1

            j = lo
            xj = xs[j]
            hj = hs[j]

            # Intercept of the line through (xj, hj) and (x, h):
            # (hj * x - h * xj) / (x - xj)
            num = hj * x - h * xj
            den = x - xj

            if best_num is None:
                best_num = num
                best_den = den
            elif num * best_den > best_num * den:
                best_num = num
                best_den = den

        # Insert current point into the upper hull.
        # Pop while slope(A, B) <= slope(B, C), i.e. B is not on the upper hull.
        while len(xs) > 1:
            x2 = xs[-1]
            h2 = hs[-1]

            if edy[-1] * (x - x2) <= (h - h2) * edx[-1]:
                xs.pop()
                hs.pop()
                edx.pop()
                edy.pop()
            else:
                break

        if xs:
            edx.append(x - xs[-1])
            edy.append(h - hs[-1])

        xs.append(x)
        hs.append(h)

    if best_num is None or best_num < 0:
        sys.stdout.write("-1\n")
    elif best_num == 0:
        sys.stdout.write("0.000000000000000000\n")
    else:
        sys.stdout.write(f"{best_num / best_den:.18f}\n")


if __name__ == "__main__":
    solve()