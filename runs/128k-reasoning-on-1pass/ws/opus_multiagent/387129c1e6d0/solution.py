import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); m = int(data[pos+1]); sx = int(data[pos+2]); sy = int(data[pos+3])
    pos += 4

    xs = [0]*n
    ys = [0]*n
    for i in range(n):
        xs[i] = int(data[pos]); ys[i] = int(data[pos+1])
        pos += 2

    vsegs = []   # (x, ylo, yhi)
    hsegs = []   # (y, xlo, xhi)
    va = vsegs.append
    ha = hsegs.append

    cx = sx; cy = sy
    for _ in range(m):
        d = data[pos]; c = int(data[pos+1])
        pos += 2
        if d == b'U':
            ny = cy + c
            va((cx, cy, ny))
            cy = ny
        elif d == b'D':
            ny = cy - c
            va((cx, ny, cy))
            cy = ny
        elif d == b'R':
            nx = cx + c
            ha((cy, cx, nx))
            cx = nx
        else:  # b'L'
            nx = cx - c
            ha((cy, nx, cx))
            cx = nx

    def build(segs):
        segs.sort()
        d = {}
        ck = None
        cs = 0; ce = 0
        starts = None; ends = None
        for k, lo, hi in segs:
            if k != ck:
                if ck is not None:
                    starts.append(cs); ends.append(ce)
                ck = k
                starts = []; ends = []
                d[k] = (starts, ends)
                cs = lo; ce = hi
            else:
                if lo <= ce:
                    if hi > ce:
                        ce = hi
                else:
                    starts.append(cs); ends.append(ce)
                    cs = lo; ce = hi
        if ck is not None:
            starts.append(cs); ends.append(ce)
        return d

    vert = build(vsegs)
    horiz = build(hsegs)

    count = 0
    vget = vert.get
    hget = horiz.get
    for i in range(n):
        X = xs[i]; Y = ys[i]
        e = vget(X)
        if e is not None:
            starts, ends = e
            j = bisect_right(starts, Y) - 1
            if j >= 0 and ends[j] >= Y:
                count += 1
                continue
        e = hget(Y)
        if e is not None:
            starts, ends = e
            j = bisect_right(starts, X) - 1
            if j >= 0 and ends[j] >= X:
                count += 1

    sys.stdout.write("%d %d %d\n" % (cx, cy, count))

main()