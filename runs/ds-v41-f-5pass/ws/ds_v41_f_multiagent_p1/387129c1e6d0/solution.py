import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    sx = int(data[idx]); idx += 1
    sy = int(data[idx]); idx += 1

    houses = []
    for _ in range(N):
        x = int(data[idx]); idx += 1
        y = int(data[idx]); idx += 1
        houses.append((x, y))

    # Collect axis-aligned segments while simulating final position.
    rows = {}  # y -> list of (x_lo, x_hi) horizontal segments
    cols = {}  # x -> list of (y_lo, y_hi) vertical segments
    cx, cy = sx, sy
    for _ in range(M):
        d = data[idx]; idx += 1
        c = int(data[idx]); idx += 1
        if d == b'U':
            cols.setdefault(cx, []).append((cy, cy + c))
            cy += c
        elif d == b'D':
            cols.setdefault(cx, []).append((cy - c, cy))
            cy -= c
        elif d == b'L':
            rows.setdefault(cy, []).append((cx - c, cx))
            cx -= c
        else:  # b'R'
            rows.setdefault(cy, []).append((cx, cx + c))
            cx += c

    def merge(d):
        res = {}
        for k, lst in d.items():
            lst.sort()
            merged = []
            cl, cr = lst[0]
            for l, r in lst[1:]:
                if l <= cr:
                    if r > cr:
                        cr = r
                else:
                    merged.append((cl, cr))
                    cl, cr = l, r
            merged.append((cl, cr))
            starts = [iv[0] for iv in merged]
            res[k] = (starts, merged)
        return res

    rowm = merge(rows)
    colm = merge(cols)

    count = 0
    for x, y in houses:
        covered = False
        if y in rowm:
            starts, merged = rowm[y]
            i = bisect_right(starts, x) - 1
            if i >= 0 and merged[i][1] >= x:
                covered = True
        if not covered and x in colm:
            starts, merged = colm[x]
            i = bisect_right(starts, y) - 1
            if i >= 0 and merged[i][1] >= y:
                covered = True
        if covered:
            count += 1

    sys.stdout.write(f"{cx} {cy} {count}\n")

main()