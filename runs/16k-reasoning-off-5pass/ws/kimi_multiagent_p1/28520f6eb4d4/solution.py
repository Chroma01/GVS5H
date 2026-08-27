import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    pts = []
    idx = 1
    for _ in range(n):
        x = int(data[idx]); h = int(data[idx + 1])
        idx += 2
        pts.append((x, h))

    # Lower convex hull of processed points (x strictly increasing).
    # Maintain strictly increasing edge slopes:
    # while slope(hull[-2] -> hull[-1]) >= slope(hull[-1] -> new): pop hull[-1]
    hull = []

    # Best intercept as exact fraction bestA / bestB, bestB > 0.
    bestA = None
    bestB = 1

    def consider(j, i):
        # intercept of line through pts[j] and pts[i]: A/B, B > 0
        nonlocal bestA, bestB
        x1, y1 = pts[j]
        x2, y2 = pts[i]
        A = y1 * x2 - y2 * x1
        B = x2 - x1
        if bestA is None or A * bestB > bestA * B:
            bestA, bestB = A, B

    for i in range(n):
        xi, hi = pts[i]
        if hull:
            if len(hull) == 1:
                consider(hull[0], i)
            else:
                # Find vertex j on hull minimizing slope(j -> i).
                # slope along hull is unimodal (decreasing then increasing)
                # because hull edge slopes are strictly increasing.
                # Binary search: compare slope(mid->i) vs slope(mid+1->i).
                lo, hi_ = 0, len(hull) - 1
                while lo < hi_:
                    mid = (lo + hi_) // 2
                    x1, y1 = pts[hull[mid]]
                    x2, y2 = pts[hull[mid + 1]]
                    # slope(mid->i) <= slope(mid+1->i) ?
                    # (hi - y1)/(xi - x1) <= (hi - y2)/(xi - x2), denominators > 0
                    if (hi - y1) * (xi - x2) <= (hi - y2) * (xi - x1):
                        hi_ = mid
                    else:
                        lo = mid + 1
                consider(hull[lo], i)

        # Insert point i into lower hull
        while len(hull) >= 2:
            x1, y1 = pts[hull[-2]]
            x2, y2 = pts[hull[-1]]
            # slope(hull[-2]->hull[-1]) >= slope(hull[-1]->i) ?
            # (y2-y1)/(x2-x1) >= (hi-y2)/(xi-x2), denominators > 0
            if (y2 - y1) * (xi - x2) >= (hi - y2) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append(i)

    if bestA is None or bestA < 0:
        sys.stdout.write("-1\n")
    else:
        value = bestA / bestB
        sys.stdout.write("{:.18f}\n".format(value))

main()