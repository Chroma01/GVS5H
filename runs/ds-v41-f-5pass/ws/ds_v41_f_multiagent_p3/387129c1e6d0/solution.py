import sys
from bisect import bisect_right
from collections import defaultdict


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    N = int(next(it))
    M = int(next(it))
    sx = int(next(it))
    sy = int(next(it))

    houses = []
    for _ in range(N):
        x = int(next(it))
        y = int(next(it))
        houses.append((x, y))

    horizontal = defaultdict(list)  # key: y, value: list of [x1, x2]
    vertical = defaultdict(list)    # key: x, value: list of [y1, y2]

    x, y = sx, sy

    for _ in range(M):
        d = next(it)
        c = int(next(it))

        if d == b'L':
            nx = x - c
            horizontal[y].append((nx, x))
            x = nx
        elif d == b'R':
            nx = x + c
            horizontal[y].append((x, nx))
            x = nx
        elif d == b'D':
            ny = y - c
            vertical[x].append((ny, y))
            y = ny
        else:  # b'U'
            ny = y + c
            vertical[x].append((y, ny))
            y = ny

    def merge_all(dic):
        for key, intervals in dic.items():
            intervals.sort()
            merged = []
            left, right = intervals[0]
            for l, r in intervals[1:]:
                if l <= right + 1:
                    if r > right:
                        right = r
                else:
                    merged.append((left, right))
                    left, right = l, r
            merged.append((left, right))
            dic[key] = merged

    merge_all(horizontal)
    merge_all(vertical)

    INF = 10**30

    def contains(intervals, val):
        idx = bisect_right(intervals, (val, INF)) - 1
        return idx >= 0 and intervals[idx][1] >= val

    answer = 0
    for hx, hy in houses:
        if (hy in horizontal and contains(horizontal[hy], hx)) or \
           (hx in vertical and contains(vertical[hx], hy)):
            answer += 1

    print(x, y, answer)


if __name__ == "__main__":
    main()