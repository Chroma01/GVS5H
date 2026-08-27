import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]

    xs = [0] * n
    hs = [0] * n
    p = 1
    for i in range(n):
        xs[i] = data[p]
        hs[i] = data[p + 1]
        p += 2

    hull = []
    best_num = None
    best_den = 1

    for i in range(n):
        x = xs[i]
        h = hs[i]

        if hull:
            lo, hi = 0, len(hull) - 1

            # Find the hull point minimizing the slope to (x, h).
            while lo < hi:
                mid = (lo + hi) // 2
                a = hull[mid]
                b = hull[mid + 1]

                # slope(a) > slope(b)
                left = (h - hs[a]) * (x - xs[b])
                right = (h - hs[b]) * (x - xs[a])

                if left > right:
                    lo = mid + 1
                else:
                    hi = mid

            j = hull[lo]
            num = x * hs[j] - xs[j] * h
            den = x - xs[j]

            if best_num is None or num * best_den > best_num * den:
                best_num = num
                best_den = den

        hull.append(i)

        # Maintain the upper convex hull.
        while len(hull) >= 3:
            a, b, c = hull[-3], hull[-2], hull[-1]
            cross = (
                (xs[b] - xs[a]) * (hs[c] - hs[b])
                - (hs[b] - hs[a]) * (xs[c] - xs[b])
            )
            if cross >= 0:
                hull.pop(-2)
            else:
                break

    if best_num is None or best_num < 0:
        print(-1)
    else:
        print(f"{best_num / best_den:.18f}")


if __name__ == "__main__":
    solve()