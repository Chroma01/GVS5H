import sys
from collections import defaultdict
from bisect import bisect_right


def merge_intervals(intervals):
    intervals.sort()
    merged = []
    start, end = intervals[0]

    for left, right in intervals[1:]:
        if left <= end:
            if right > end:
                end = right
        else:
            merged.append((start, end))
            start, end = left, right

    merged.append((start, end))
    return merged


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0

    n = int(data[pos])
    pos += 1
    m = int(data[pos])
    pos += 1
    sx = int(data[pos])
    pos += 1
    sy = int(data[pos])
    pos += 1

    rows = defaultdict(list)  # y -> [(x, house_id)]
    cols = defaultdict(list)  # x -> [(y, house_id)]

    for house_id in range(n):
        x = int(data[pos])
        y = int(data[pos + 1])
        pos += 2
        rows[y].append((x, house_id))
        cols[x].append((y, house_id))

    horizontal = defaultdict(list)  # y -> [(left, right)]
    vertical = defaultdict(list)    # x -> [(bottom, top)]

    x, y = sx, sy

    for _ in range(m):
        direction = data[pos]
        distance = int(data[pos + 1])
        pos += 2

        if direction == b'L':
            horizontal[y].append((x - distance, x))
            x -= distance
        elif direction == b'R':
            horizontal[y].append((x, x + distance))
            x += distance
        elif direction == b'D':
            vertical[x].append((y - distance, y))
            y -= distance
        else:  # U
            vertical[x].append((y, y + distance))
            y += distance

    for houses in rows.values():
        houses.sort()
    for houses in cols.values():
        houses.sort()

    visited = [False] * n
    count = 0

    for fixed_y, houses in rows.items():
        intervals = horizontal.get(fixed_y)
        if not intervals:
            continue

        merged = merge_intervals(intervals)
        starts = [left for left, _ in merged]
        ends = [right for _, right in merged]

        for house_x, house_id in houses:
            index = bisect_right(starts, house_x) - 1
            if index >= 0 and house_x <= ends[index]:
                if not visited[house_id]:
                    visited[house_id] = True
                    count += 1

    for fixed_x, houses in cols.items():
        intervals = vertical.get(fixed_x)
        if not intervals:
            continue

        merged = merge_intervals(intervals)
        starts = [bottom for bottom, _ in merged]
        ends = [top for _, top in merged]

        for house_y, house_id in houses:
            if visited[house_id]:
                continue
            index = bisect_right(starts, house_y) - 1
            if index >= 0 and house_y <= ends[index]:
                visited[house_id] = True
                count += 1

    print(x, y, count)


if __name__ == "__main__":
    main()