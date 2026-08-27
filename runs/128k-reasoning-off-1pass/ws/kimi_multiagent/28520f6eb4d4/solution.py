import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = [0] * n
    H = [0] * n
    idx = 1
    for i in range(n):
        X[i] = int(data[idx]); H[i] = int(data[idx + 1])
        idx += 2

    hx = []  # hull x-coords (upper hull of building tops)
    hh = []  # hull heights

    best_num = None
    best_den = 1

    for i in range(n):
        xp = X[i]; hp = H[i]
        m = len(hx)
        if m:
            # Binary search for vertex minimizing slope from P=(xp,hp).
            # p(k): f(k+1) > f(k)  <=>  P strictly above line of edge (k,k+1).
            # Predicate is monotone (False...False True...True); min vertex =
            # first k with p(k) true, else last vertex.
            if m == 1:
                k = 0
            else:
                lo = 0
                hi = m - 1  # answer vertex index; default m-1 if all False
                while lo < hi:
                    mid = (lo + hi) >> 1
                    # edge (mid, mid+1): line value at xp, scaled by dx (>0)
                    dx = hx[mid + 1] - hx[mid]
                    line_val = (hh[mid + 1] - hh[mid]) * xp \
                        + hh[mid] * hx[mid + 1] - hh[mid + 1] * hx[mid]
                    if hp * dx > line_val:
                        hi = mid
                    else:
                        lo = mid + 1
                k = lo
            num = xp * hh[k] - hp * hx[k]
            den = xp - hx[k]
            if best_num is None or num * best_den > best_num * den:
                best_num = num
                best_den = den

        # Append (xp, hp) to upper hull: pop while middle point is on or below
        # the line from second-last to new point (cross >= 0).
        while len(hx) >= 2:
            cross = (hx[-1] - hx[-2]) * (hp - hh[-2]) \
                  - (hh[-1] - hh[-2]) * (xp - hx[-2])
            if cross >= 0:
                hx.pop(); hh.pop()
            else:
                break
        hx.append(xp); hh.append(hp)

    if best_num is None or best_num < 0:
        sys.stdout.write("-1\n")
    elif best_num == 0:
        sys.stdout.write("0.000000000000000000\n")
    else:
        sys.stdout.write("{:.18f}\n".format(best_num / best_den))

main()