import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = [0]*(n+1)
    H = [0]*(n+1)
    idx = 1
    for i in range(1, n+1):
        X[i] = int(data[idx]); H[i] = int(data[idx+1]); idx += 2

    hx = []  # hull x coords (increasing)
    hy = []  # hull y coords

    best_num = None
    best_den = 1

    def cross(ox, oy, ax, ay, bx, by):
        return (ax-ox)*(by-oy) - (ay-oy)*(bx-ox)

    for i in range(1, n+1):
        xi, hi = X[i], H[i]
        if hx:
            # f(j) = intercept of line through (hx[j],hy[j]) and (xi,hi):
            # b = (hy[j]*xi - hi*hx[j]) / (xi - hx[j]), denominator > 0.
            # Unimodal on the upper hull; binary search comparing neighbors.
            lo, r = 0, len(hx)-1
            while lo < r:
                mid = (lo + r)//2
                n1 = hy[mid]*xi - hi*hx[mid]
                d1 = xi - hx[mid]
                n2 = hy[mid+1]*xi - hi*hx[mid+1]
                d2 = xi - hx[mid+1]
                if n1*d2 < n2*d1:
                    lo = mid+1
                else:
                    r = mid
            j = lo
            num = hy[j]*xi - hi*hx[j]
            den = xi - hx[j]
            if best_num is None or num*best_den > best_num*den:
                best_num, best_den = num, den
        # insert (xi,hi) into upper hull; pop while turn is non-counterclockwise
        while len(hx) >= 2 and cross(hx[-2], hy[-2], hx[-1], hy[-1], xi, hi) >= 0:
            hx.pop(); hy.pop()
        hx.append(xi); hy.append(hi)

    if best_num is None or best_num < 0:
        sys.stdout.write("-1\n")
    else:
        sys.stdout.write("{:.15f}\n".format(best_num / best_den))

solve()