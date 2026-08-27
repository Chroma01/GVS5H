import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    points = [(data[i], data[i + 1]) for i in range(1, 2 * n + 1, 2)]

    if n == 1:
        print(-1)
        return

    # Upper convex hull of already processed points.
    hull = []

    # Maximum blocking threshold as exact fraction best_num / best_den.
    best_num = None
    best_den = 1

    for xi, hi in points:
        if hull:
            # The slopes from upper-hull vertices to (xi, hi) are unimodal.
            # Find a vertex giving the minimum slope.
            lo = 0
            r = len(hull) - 1
            while lo < r:
                mid = (lo + r) // 2
                x1, h1 = hull[mid]
                x2, h2 = hull[mid + 1]

                # Is slope((x1,h1), target) <= slope((x2,h2), target)?
                if (hi - h1) * (xi - x2) <= (hi - h2) * (xi - x1):
                    r = mid
                else:
                    lo = mid + 1

            xj, hj = hull[lo]

            # Observer height at which top j lies on the sight line to top i.
            num = xi * hj - xj * hi
            den = xi - xj

            if best_num is None or num * best_den > best_num * den:
                best_num = num
                best_den = den

        # Maintain an upper hull whose consecutive edge slopes decrease strictly.
        while len(hull) >= 2:
            xa, ha = hull[-2]
            xb, hb = hull[-1]

            # Remove b if slope(a,b) <= slope(b,current).
            if (xb - xa) * (hi - hb) - (hb - ha) * (xi - xb) >= 0:
                hull.pop()
            else:
                break

        hull.append((xi, hi))

    if best_num < 0:
        print(-1)
    else:
        print("{:.18f}".format(best_num / best_den))


if __name__ == "__main__":
    solve()