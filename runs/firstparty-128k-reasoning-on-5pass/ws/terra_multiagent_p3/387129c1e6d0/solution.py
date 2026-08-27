import sys
from collections import defaultdict
from bisect import bisect_left, bisect_right

def merge_intervals(intervals):
    intervals.sort()
    merged = []
    left, right = intervals[0]
    for a, b in intervals[1:]:
        if a <= right + 1:
            if b > right:
                right = b
        else:
            merged.append((left, right))
            left, right = a, b
    merged.append((left, right))
    return merged

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    x = int(next(it))
    y = int(next(it))

    houses_by_y = defaultdict(list)
    houses_by_x = defaultdict(list)

    for idx in range(n):
        hx = int(next(it))
        hy = int(next(it))
        houses_by_y[hy].append((hx, idx))
        houses_by_x[hx].append((hy, idx))

    horizontal = defaultdict(list)
    vertical = defaultdict(list)

    for _ in range(m):
        d = next(it)
        c = int(next(it))

        if d == b'U':
            ny = y + c
            vertical[x].append((y, ny))
            y = ny
        elif d == b'D':
            ny = y - c
            vertical[x].append((ny, y))
            y = ny
        elif d == b'R':
            nx = x + c
            horizontal[y].append((x, nx))
            x = nx
        else:  # L
            nx = x - c
            horizontal[y].append((nx, x))
            x = nx

    visited = [False] * n
    count = 0

    for fixed_y, intervals in horizontal.items():
        points = houses_by_y.get(fixed_y)
        if not points:
            continue

        points.sort()
        coords = [px for px, _ in points]

        for left, right in merge_intervals(intervals):
            lo = bisect_left(coords, left)
            hi = bisect_right(coords, right)
            for j in range(lo, hi):
                idx = points[j][1]
                if not visited[idx]:
                    visited[idx] = True
                    count += 1

    for fixed_x, intervals in vertical.items():
        points = houses_by_x.get(fixed_x)
        if not points:
            continue

        points.sort()
        coords = [py for py, _ in points]

        for left, right in merge_intervals(intervals):
            lo = bisect_left(coords, left)
            hi = bisect_right(coords, right)
            for j in range(lo, hi):
                idx = points[j][1]
                if not visited[idx]:
                    visited[idx] = True
                    count += 1

    print(x, y, count)

if __name__ == "__main__":
    main()