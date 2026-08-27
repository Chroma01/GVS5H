import sys
from bisect import bisect_right
from collections import defaultdict


def main():
    tokens = sys.stdin.buffer.read().split()
    it = iter(tokens)

    n = int(next(it))
    m = int(next(it))
    sx = int(next(it))
    sy = int(next(it))

    houses = []
    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        houses.append((x, y))

    horizontal = defaultdict(list)  # y -> [(left, right), ...]
    vertical = defaultdict(list)    # x -> [(bottom, top), ...]

    x, y = sx, sy

    for _ in range(m):
        direction = next(it)
        length = int(next(it))

        if direction == b"L":
            horizontal[y].append((x - length, x))
            x -= length
        elif direction == b"R":
            horizontal[y].append((x, x + length))
            x += length
        elif direction == b"D":
            vertical[x].append((y - length, y))
            y -= length
        else:  # U
            vertical[x].append((y, y + length))
            y += length

    def merge(intervals):
        intervals.sort()
        merged = []
        for left, right in intervals:
            if merged and left <= merged[-1][1] + 1:
                if right > merged[-1][1]:
                    merged[-1] = (merged[-1][0], right)
            else:
                merged.append((left, right))
        starts = [interval[0] for interval in merged]
        ends = [interval[1] for interval in merged]
        return starts, ends

    for key in list(horizontal):
        horizontal[key] = merge(horizontal[key])
    for key in list(vertical):
        vertical[key] = merge(vertical[key])

    def covered(interval_map, key, point):
        data = interval_map.get(key)
        if data is None:
            return False
        starts, ends = data
        index = bisect_right(starts, point) - 1
        return index >= 0 and point <= ends[index]

    count = 0
    for hx, hy in houses:
        if covered(horizontal, hy, hx) or covered(vertical, hx, hy):
            count += 1

    print(x, y, count)


if __name__ == "__main__":
    main()