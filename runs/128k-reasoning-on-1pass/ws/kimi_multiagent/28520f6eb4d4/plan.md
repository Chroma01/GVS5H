```python
import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    pts = [(data[i], data[i + 1]) for i in range(1, 2 * n + 1, 2)]

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def slope_less(i, j, q):
        xi, yi = hull[i]
        xj, yj = hull[j]
        xq, yq = q
        return (yq - yi) * (xq - xj) < (yq - yj) * (xq - xi)

    hull = []
    best_num = None
    best_den = 1

    for x, y in pts:
        if hull:
            lo, hi = 0, len(hull) - 1
            q = (x, y)
            while lo < hi:
                mid = (lo + hi) // 2
                if slope_less(mid, mid + 1, q):
                    hi = mid
                else:
                    lo = mid + 1
            xj, yj = hull[lo]
            num = x * yj - xj * y
            den = x - xj
            if best_num is None or num * best_den > best_num * den:
                best_num, best_den = num, den

        p = (x, y)
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) >= 0:
            hull.pop()
        hull.append(p)

    if best_num is None or best_num < 0:
        sys.stdout.write("-1\n")
    else:
        sys.stdout.write("{:.18f}\n".format(best_num / best_den))

main()
```