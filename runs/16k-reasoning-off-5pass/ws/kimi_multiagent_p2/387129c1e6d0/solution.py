import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    x = int(data[idx]); idx += 1
    y = int(data[idx]); idx += 1

    xs = [0] * N
    ys = [0] * N
    by_x = defaultdict(list)  # x -> sorted list of (y, house_index)
    by_y = defaultdict(list)  # y -> sorted list of (x, house_index)
    for i in range(N):
        xi = int(data[idx]); idx += 1
        yi = int(data[idx]); idx += 1
        xs[i] = xi
        ys[i] = yi
        by_x[xi].append((yi, i))
        by_y[yi].append((xi, i))

    for lst in by_x.values():
        lst.sort()
    for lst in by_y.values():
        lst.sort()

    visited = set()

    for _ in range(M):
        d = data[idx].decode(); idx += 1
        c = int(data[idx]); idx += 1
        if d == 'U':
            nx, ny = x, y + c
            lst = by_x.get(x)
            if lst:
                lo = bisect_left(lst, (y, -1))
                hi = bisect_right(lst, (ny, N))
                for j in range(lo, hi):
                    visited.add(lst[j][1])
        elif d == 'D':
            nx, ny = x, y - c
            lst = by_x.get(x)
            if lst:
                lo = bisect_left(lst, (ny, -1))
                hi = bisect_right(lst, (y, N))
                for j in range(lo, hi):
                    visited.add(lst[j][1])
        elif d == 'L':
            nx, ny = x - c, y
            lst = by_y.get(y)
            if lst:
                lo = bisect_left(lst, (nx, -1))
                hi = bisect_right(lst, (x, N))
                for j in range(lo, hi):
                    visited.add(lst[j][1])
        else:  # 'R'
            nx, ny = x + c, y
            lst = by_y.get(y)
            if lst:
                lo = bisect_left(lst, (x, -1))
                hi = bisect_right(lst, (nx, N))
                for j in range(lo, hi):
                    visited.add(lst[j][1])
        x, y = nx, ny

    sys.stdout.write(f"{x} {y} {len(visited)}\n")

main()