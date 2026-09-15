import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    if N == 1:
        print(-1)
        return

    pts = [(data[1 + 2 * i], data[2 + 2 * i]) for i in range(N)]

    hx = []
    hy = []
    best_num = None
    best_den = 1

    for X, Y in pts:
        if hx:
            lo = 0
            hi = len(hx) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                x1 = hx[mid]
                y1 = hy[mid]
                x2 = hx[mid + 1]
                y2 = hy[mid + 1]
                # Check if edge slope <= slope from hull[mid] to new point
                if (y2 - y1) * (X - x1) <= (Y - y1) * (x2 - x1):
                    hi = mid
                else:
                    lo = mid + 1
            idx = lo
            xj = hx[idx]
            yj = hy[idx]
            # Intercept b = (yj * X - Y * xj) / (X - xj)
            num = yj * X - Y * xj
            den = X - xj
            if best_num is None or num * best_den > best_num * den:
                best_num = num
                best_den = den

        # Insert new point into upper convex hull
        while len(hx) >= 2:
            x1 = hx[-2]
            y1 = hy[-2]
            x2 = hx[-1]
            y2 = hy[-1]
            # Pop if slope(hull[-2] -> hull[-1]) <= slope(hull[-1] -> new)
            if (y2 - y1) * (X - x2) <= (Y - y2) * (x2 - x1):
                hx.pop()
                hy.pop()
            else:
                break
        hx.append(X)
        hy.append(Y)

    if best_num is None or best_num < 0:
        print(-1)
    else:
        print(f"{best_num / best_den:.18f}")

if __name__ == "__main__":
    main()