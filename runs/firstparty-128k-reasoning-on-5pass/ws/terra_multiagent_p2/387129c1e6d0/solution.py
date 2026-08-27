import sys
from bisect import bisect_right

def merge_intervals(groups):
    for key, intervals in groups.items():
        intervals.sort()
        merged = []
        left, right = intervals[0]
        for l, r in intervals[1:]:
            if l <= right:
                if r > right:
                    right = r
            else:
                merged.append((left, right))
                left, right = l, r
        merged.append((left, right))
        groups[key] = merged

def covered(intervals, value):
    if not intervals:
        return False
    i = bisect_right(intervals, (value, 10**30)) - 1
    return i >= 0 and value <= intervals[i][1]

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    x = int(next(it))
    y = int(next(it))

    houses = []
    for _ in range(n):
        hx = int(next(it))
        hy = int(next(it))
        houses.append((hx, hy))

    horizontal = {}
    vertical = {}

    for _ in range(m):
        d = next(it)
        c = int(next(it))

        if d == b'L':
            nx = x - c
            l, r = nx, x
            horizontal.setdefault(y, []).append((l, r))
            x = nx
        elif d == b'R':
            nx = x + c
            l, r = x, nx
            horizontal.setdefault(y, []).append((l, r))
            x = nx
        elif d == b'D':
            ny = y - c
            l, r = ny, y
            vertical.setdefault(x, []).append((l, r))
            y = ny
        else:  # U
            ny = y + c
            l, r = y, ny
            vertical.setdefault(x, []).append((l, r))
            y = ny

    merge_intervals(horizontal)
    merge_intervals(vertical)

    count = 0
    for hx, hy in houses:
        if covered(horizontal.get(hy), hx) or covered(vertical.get(hx), hy):
            count += 1

    print(x, y, count)

if __name__ == "__main__":
    main()