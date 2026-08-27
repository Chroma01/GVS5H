import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    sx = int(next(it))
    sy = int(next(it))

    horizontal_houses = {}
    vertical_houses = {}

    for house_id in range(n):
        x = int(next(it))
        y = int(next(it))
        horizontal_houses.setdefault(y, []).append((x, house_id))
        vertical_houses.setdefault(x, []).append((y, house_id))

    horizontal_segments = {}
    vertical_segments = {}

    x, y = sx, sy

    for _ in range(m):
        direction = next(it)
        distance = int(next(it))

        if direction == b'L':
            nx = x - distance
            horizontal_segments.setdefault(y, []).append((nx, x))
            x = nx
        elif direction == b'R':
            nx = x + distance
            horizontal_segments.setdefault(y, []).append((x, nx))
            x = nx
        elif direction == b'D':
            ny = y - distance
            vertical_segments.setdefault(x, []).append((ny, y))
            y = ny
        else:  # U
            ny = y + distance
            vertical_segments.setdefault(x, []).append((y, ny))
            y = ny

    visited = bytearray(n)
    count = 0

    def process_segments(segments, houses):
        nonlocal count

        for fixed_coordinate, intervals in segments.items():
            house_list = houses.get(fixed_coordinate)
            if not house_list:
                continue

            intervals.sort()
            merged = []
            left, right = intervals[0]

            for next_left, next_right in intervals[1:]:
                if next_left <= right:
                    if next_right > right:
                        right = next_right
                else:
                    merged.append((left, right))
                    left, right = next_left, next_right
            merged.append((left, right))

            for left, right in merged:
                begin = bisect_left(house_list, (left, -1))
                end = bisect_right(house_list, (right, n))
                for i in range(begin, end):
                    house_id = house_list[i][1]
                    if not visited[house_id]:
                        visited[house_id] = 1
                        count += 1

    for house_list in horizontal_houses.values():
        house_list.sort()
    for house_list in vertical_houses.values():
        house_list.sort()

    process_segments(horizontal_segments, horizontal_houses)
    process_segments(vertical_segments, vertical_houses)

    print(x, y, count)


if __name__ == "__main__":
    main()