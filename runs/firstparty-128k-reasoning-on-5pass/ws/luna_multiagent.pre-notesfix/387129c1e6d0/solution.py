import sys
from collections import defaultdict
from bisect import bisect_right


def merge_intervals(groups):
    merged = {}
    for key, intervals in groups.items():
        intervals.sort()
        result = []
        left, right = intervals[0]

        for nl, nr in intervals[1:]:
            if nl <= right + 1:
                if nr > right:
                    right = nr
            else:
                result.append((left, right))
                left, right = nl, nr

        result.append((left, right))
        merged[key] = result
    return merged


def covered(intervals, value):
    if not intervals:
        return False

    idx = bisect_right(intervals, (value, 10**30)) - 1
    return idx >= 0 and intervals[idx][0] <= value <= intervals[idx][1]


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    sx = int(next(it))
    sy = int(next(it))

    houses = []
    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        houses.append((x, y))

    horizontal = defaultdict(list)  # y -> intervals of x
    vertical = defaultdict(list)    # x -> intervals of y

    x, y = sx, sy

    for _ in range(m):
        direction = next(it)
        length = int(next(it))

        if direction == b'L':
            nx = x - length
            horizontal[y].append((min(x, nx), max(x, nx)))
            x = nx
        elif direction == b'R':
            nx = x + length
            horizontal[y].append((min(x, nx), max(x, nx)))
            x = nx
        elif direction == b'D':
            ny = y - length
            vertical[x].append((min(y, ny), max(y, ny)))
            y = ny
        else:  # U
            ny = y + length
            vertical[x].append((min(y, ny), max(y, ny)))
            y = ny

    horizontal = merge_intervals(horizontal)
    vertical = merge_intervals(vertical)

    count = 0
    for hx, hy in houses:
        if covered(horizontal.get(hy), hx) or covered(vertical.get(hx), hy):
            count += 1

    print(x, y, count)


if __name__ == "__main__":
    main()