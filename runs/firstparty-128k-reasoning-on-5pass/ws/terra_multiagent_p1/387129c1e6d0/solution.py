import sys
from bisect import bisect_right

def build_merged_index(segments):
    """
    segments: list of (fixed_coordinate, left, right)
    Returns:
      index[fixed_coordinate] = (offset, count)
      starts, ends: flattened merged inclusive intervals
    """
    if not segments:
        return {}, [], []

    segments.sort()

    index = {}
    starts = []
    ends = []

    i = 0
    n = len(segments)

    while i < n:
        fixed = segments[i][0]
        offset = len(starts)

        left = segments[i][1]
        right = segments[i][2]
        i += 1

        while i < n and segments[i][0] == fixed:
            _, nl, nr = segments[i]
            if nl <= right + 1:
                if nr > right:
                    right = nr
            else:
                starts.append(left)
                ends.append(right)
                left, right = nl, nr
            i += 1

        starts.append(left)
        ends.append(right)
        index[fixed] = (offset, len(starts) - offset)

    return index, starts, ends


def covered(index, starts, ends, fixed, value):
    info = index.get(fixed)
    if info is None:
        return False

    offset, count = info
    pos = bisect_right(starts, value, offset, offset + count) - 1
    return pos >= offset and value <= ends[pos]


def main():
    input = sys.stdin.buffer.readline

    n, m, sx, sy = map(int, input().split())
    houses = [tuple(map(int, input().split())) for _ in range(n)]

    horizontal = []
    vertical = []

    x, y = sx, sy

    for _ in range(m):
        d, c = input().split()
        c = int(c)

        if d == b'U':
            ny = y + c
            vertical.append((x, y, ny))
            y = ny
        elif d == b'D':
            ny = y - c
            vertical.append((x, ny, y))
            y = ny
        elif d == b'R':
            nx = x + c
            horizontal.append((y, x, nx))
            x = nx
        else:  # L
            nx = x - c
            horizontal.append((y, nx, x))
            x = nx

    h_index, h_starts, h_ends = build_merged_index(horizontal)
    v_index, v_starts, v_ends = build_merged_index(vertical)

    count = 0
    for hx, hy in houses:
        if covered(h_index, h_starts, h_ends, hy, hx):
            count += 1
        elif covered(v_index, v_starts, v_ends, hx, hy):
            count += 1

    print(x, y, count)


if __name__ == "__main__":
    main()