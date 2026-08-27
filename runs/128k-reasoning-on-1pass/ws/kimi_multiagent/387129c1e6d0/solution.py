import sys
import bisect

INF = 10**30


def merge_intervals(mp):
    merged_map = {}
    for key, intervals in mp.items():
        intervals.sort()
        merged = []
        for l, r in intervals:
            if merged and l <= merged[-1][1] + 1:
                if r > merged[-1][1]:
                    merged[-1] = (merged[-1][0], r)
            else:
                merged.append((l, r))
        merged_map[key] = merged
    return merged_map


def contains(intervals, v):
    # Rightmost interval with left endpoint <= v.
    i = bisect.bisect_right(intervals, (v, INF)) - 1
    return i >= 0 and intervals[i][1] >= v


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    p = 0
    N = int(data[p]); M = int(data[p + 1])
    x = int(data[p + 2]); y = int(data[p + 3])
    p += 4

    houses = []
    for _ in range(N):
        hx = int(data[p]); hy = int(data[p + 1])
        p += 2
        houses.append((hx, hy))

    horizontal = {}  # y -> list of inclusive x-intervals
    vertical = {}    # x -> list of inclusive y-intervals

    for _ in range(M):
        d = data[p]
        c = int(data[p + 1])
        p += 2

        if d == b'U':
            ny = y + c
            vertical.setdefault(x, []).append((y, ny))
            y = ny
        elif d == b'D':
            ny = y - c
            vertical.setdefault(x, []).append((ny, y))
            y = ny
        elif d == b'L':
            nx = x - c
            horizontal.setdefault(y, []).append((nx, x))
            x = nx
        else:  # b'R'
            nx = x + c
            horizontal.setdefault(y, []).append((x, nx))
            x = nx

    horizontal = merge_intervals(horizontal)
    vertical = merge_intervals(vertical)

    count = 0
    for hx, hy in houses:
        iv = horizontal.get(hy)
        if iv is not None and contains(iv, hx):
            count += 1
            continue

        iv = vertical.get(hx)
        if iv is not None and contains(iv, hy):
            count += 1

    sys.stdout.write(f"{x} {y} {count}\n")


if __name__ == "__main__":
    main()