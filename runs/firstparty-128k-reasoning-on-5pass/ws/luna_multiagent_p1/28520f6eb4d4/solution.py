import sys


def solve():
    input = sys.stdin.buffer.readline
    n = int(input())

    xs = [0] * n
    hs = [0] * n
    for i in range(n):
        xs[i], hs[i] = map(int, input().split())

    # Upper convex hull of previously processed buildings.
    hull = []

    best_num = None
    best_den = 1

    for i in range(n):
        x, h = xs[i], hs[i]

        if hull:
            # The intercept values obtained from hull points are unimodal.
            # Find the first adjacent pair where the left value is at least
            # the right value.
            lo, hi = 0, len(hull) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                xa, ha = hull[mid]
                xb, hb = hull[mid + 1]

                # orient((x, h), (xa, ha), (xb, hb))
                # Its sign equals the sign of T(xa, ha) - T(xb, hb).
                orient = (xa - x) * (hb - h) - (ha - h) * (xb - x)

                if orient >= 0:
                    hi = mid
                else:
                    lo = mid + 1

            xj, hj = hull[lo]
            num = x * hj - xj * h
            den = x - xj

            if best_num is None or num * best_den > best_num * den:
                best_num = num
                best_den = den

        # Maintain the upper hull.  Collinear middle points are unnecessary.
        while len(hull) >= 2:
            xa, ha = hull[-2]
            xb, hb = hull[-1]

            cross = (xb - xa) * (h - ha) - (hb - ha) * (x - xa)
            if cross >= 0:
                hull.pop()
            else:
                break

        hull.append((x, h))

    # With no pair, or with a negative maximum threshold, height 0 sees all.
    if best_num is None or best_num < 0:
        print(-1)
    else:
        print(f"{best_num / best_den:.18f}")


if __name__ == "__main__":
    solve()