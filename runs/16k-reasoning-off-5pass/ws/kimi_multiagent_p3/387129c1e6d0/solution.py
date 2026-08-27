import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict

def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); M = int(data[p+1]); Sx = int(data[p+2]); Sy = int(data[p+3])
    p += 4

    by_y = defaultdict(list)  # y -> list of (x, idx)
    by_x = defaultdict(list)  # x -> list of (y, idx)
    for i in range(N):
        x = int(data[p]); y = int(data[p+1]); p += 2
        by_y[y].append((x, i))
        by_x[x].append((y, i))

    for lst in by_y.values():
        lst.sort()
    for lst in by_x.values():
        lst.sort()

    visited = set()
    x, y = Sx, Sy

    for _ in range(M):
        d = data[p]; c = int(data[p+1]); p += 2
        if d == b'U':
            ny = y + c
            lst = by_x.get(x)
            if lst:
                lo = bisect_left(lst, (y, -1))
                hi = bisect_right(lst, (ny, N))
                for j in range(lo, hi):
                    visited.add(lst[j][1])
            y = ny
        elif d == b'D':
            ny = y - c
            lst = by_x.get(x)
            if lst:
                lo = bisect_left(lst, (ny, -1))
                hi = bisect_right(lst, (y, N))
                for j in range(lo, hi):
                    visited.add(lst[j][1])
            y = ny
        elif d == b'L':
            nx = x - c
            lst = by_y.get(y)
            if lst:
                lo = bisect_left(lst, (nx, -1))
                hi = bisect_right(lst, (x, N))
                for j in range(lo, hi):
                    visited.add(lst[j][1])
            x = nx
        else:  # R
            nx = x + c
            lst = by_y.get(y)
            if lst:
                lo = bisect_left(lst, (x, -1))
                hi = bisect_right(lst, (nx, N))
                for j in range(lo, hi):
                    visited.add(lst[j][1])
            x = nx

    sys.stdout.write(f"{x} {y} {len(visited)}\n")

main()