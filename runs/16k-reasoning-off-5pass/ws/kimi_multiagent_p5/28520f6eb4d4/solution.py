import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = [0]*n
    H = [0]*n
    idx = 1
    for i in range(n):
        X[i] = int(data[idx]); H[i] = int(data[idx+1]); idx += 2

    # Upper convex hull of points (X_j, H_j) with strictly increasing x.
    hx = []
    hy = []

    # Best (maximum) intercept seen so far, as exact fraction best_num/best_den.
    best_num = None
    best_den = 1

    for i in range(n):
        xi, hi = X[i], H[i]
        if hx:
            # Binary search the hull vertex k maximizing the y-intercept of the
            # line through (hx[k], hy[k]) and (xi, hi):
            #   intercept(k) = (hy[k]*xi - hi*hx[k]) / (xi - hx[k])
            # The sequence of intercepts along the hull is unimodal, so compare
            # adjacent vertices and move toward the larger one.
            lo, r = 0, len(hx) - 1
            while lo < r:
                mid = (lo + r) // 2
                x1, y1 = hx[mid], hy[mid]
                x2, y2 = hx[mid+1], hy[mid+1]
                n1 = y1*xi - hi*x1
                d1 = xi - x1
                n2 = y2*xi - hi*x2
                d2 = xi - x2
                # intercept(mid+1) > intercept(mid)  <=>  n2/d2 > n1/d1
                if n2*d1 > n1*d2:
                    lo = mid + 1
                else:
                    r = mid
            k = lo
            num = hy[k]*xi - hi*hx[k]
            den = xi - hx[k]
            if best_num is None or num*best_den > best_num*den:
                best_num, best_den = num, den

        # Append (xi, hi) to the upper hull, removing vertices that lie on or
        # below the segment from the second-to-last vertex to the new point.
        while len(hx) >= 2:
            x1, y1 = hx[-2], hy[-2]
            x2, y2 = hx[-1], hy[-1]
            # Upper hull with increasing x: pop middle if
            # slope((x1,y1)->(x2,y2)) <= slope((x2,y2)->(xi,hi))
            if (y2-y1)*(xi-x2) <= (hi-y2)*(x2-x1):
                hx.pop(); hy.pop()
            else:
                break
        hx.append(xi); hy.append(hi)

    if best_num is None or best_num < 0:
        # All buildings strictly visible already at h = 0.
        sys.stdout.write("-1\n")
    else:
        ans = best_num / best_den
        sys.stdout.write("{:.15f}\n".format(ans))

solve()