import sys


def solve():
    input = sys.stdin.readline
    n = int(input())

    xs = [0] * n
    hs = [0] * n

    # Lower convex hull of previously processed points (X, H).
    hull = []

    best_num = None
    best_den = 1

    for i in range(n):
        x, h = map(int, input().split())
        xs[i] = x
        hs[i] = h

        if hull:
            # For hull index k, slope from point k to current point is:
            # (h - H[k]) / (x - X[k]).
            def slope_leq(a, b):
                return ((h - hs[hull[a]]) * (x - xs[hull[b]]) <=
                        (h - hs[hull[b]]) * (x - xs[hull[a]]))

            # Slopes along the lower hull are unimodal from the current point.
            lo, hi = 0, len(hull) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                if slope_leq(mid, mid + 1):
                    hi = mid
                else:
                    lo = mid + 1

            j = hull[lo]

            # Critical height where current and j have equal top viewing slope:
            # (h - y) / x = (H[j] - y) / X[j]
            num = x * hs[j] - xs[j] * h
            den = x - xs[j]

            if best_num is None or num * best_den > best_num * den:
                best_num = num
                best_den = den

        # Insert current point into the lower convex hull.
        while len(hull) >= 2:
            a = hull[-2]
            b = hull[-1]
            cross = ((xs[b] - xs[a]) * (h - hs[a]) -
                     (hs[b] - hs[a]) * (x - xs[a]))
            if cross <= 0:
                hull.pop()
            else:
                break
        hull.append(i)

    if best_num is None or best_num < 0:
        print(-1)
    else:
        print("{:.18f}".format(best_num / best_den))


if __name__ == "__main__":
    solve()