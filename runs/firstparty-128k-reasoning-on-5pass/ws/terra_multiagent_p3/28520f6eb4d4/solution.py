import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    points = [(data[i], data[i + 1]) for i in range(1, 2 * n + 1, 2)]

    if n == 1:
        print(-1)
        return

    hull = [points[0]]
    ptr = 0

    best_num = None
    best_den = 1

    for i in range(1, n):
        x, h = points[i]

        # Advance to the lower-hull vertex having the minimum slope to (x, h).
        while ptr + 1 < len(hull):
            xa, ha = hull[ptr]
            xb, hb = hull[ptr + 1]

            # slope((xb,hb),(x,h)) <= slope((xa,ha),(x,h))
            if (h - hb) * (x - xa) <= (h - ha) * (x - xb):
                ptr += 1
            else:
                break

        xj, hj = hull[ptr]
        num = x * hj - xj * h
        den = x - xj

        if best_num is None or num * best_den > best_num * den:
            best_num = num
            best_den = den

        # Insert current point into the lower convex hull.
        while len(hull) >= 2:
            xa, ha = hull[-2]
            xb, hb = hull[-1]

            # slope(a,b) >= slope(b,current): b is unnecessary.
            if (hb - ha) * (x - xb) >= (h - hb) * (xb - xa):
                hull.pop()
                if ptr >= len(hull):
                    ptr = len(hull) - 1
            else:
                break

        hull.append((x, h))

    # At height 0, every building is visible iff every threshold is strictly negative.
    if best_num < 0:
        print(-1)
    else:
        print(f"{best_num / best_den:.18f}")

if __name__ == "__main__":
    main()