import sys


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    points = [(data[i], data[i + 1]) for i in range(1, 2 * n + 1, 2)]

    hull = []
    best_num = None
    best_den = 1

    for x, h in points:
        if hull:
            lo, hi = 0, len(hull) - 1

            # Find the vertex minimizing (h - hull_y) / (x - hull_x).
            while lo < hi:
                mid = (lo + hi) // 2
                a = hull[mid]
                b = hull[mid + 1]

                left = (h - a[1]) * (x - b[0])
                right = (h - b[1]) * (x - a[0])

                if left <= right:
                    hi = mid
                else:
                    lo = mid + 1

            px, py = hull[lo]
            num = x * py - px * h
            den = x - px

            if best_num is None or num * best_den > best_num * den:
                best_num = num
                best_den = den

        new_point = (x, h)
        while len(hull) >= 2 and cross(hull[-2], hull[-1], new_point) >= 0:
            hull.pop()
        hull.append(new_point)

    if best_num is None or best_num < 0:
        print(-1)
    else:
        print("{:.18f}".format(best_num / best_den))


if __name__ == "__main__":
    solve()