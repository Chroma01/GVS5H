import sys
from bisect import bisect_left, bisect_right


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def main():
    tokens = sys.stdin.buffer.read().split()
    it = iter(tokens)

    n = int(next(it))
    m = int(next(it))
    sx = int(next(it))
    sy = int(next(it))

    xs = [0] * n
    ys = [0] * n
    rows = {}
    cols = {}

    for i in range(n):
        x = int(next(it))
        y = int(next(it))
        xs[i] = x
        ys[i] = y
        rows.setdefault(y, []).append((x, i))
        cols.setdefault(x, []).append((y, i))

    row_idx = [0] * n
    col_idx = [0] * n

    for y, houses in list(rows.items()):
        houses.sort()
        coords = [p[0] for p in houses]
        ids = [p[1] for p in houses]
        parent = list(range(len(coords) + 1))
        rows[y] = (coords, parent, ids)
        for j, house_id in enumerate(ids):
            row_idx[house_id] = j

    for x, houses in list(cols.items()):
        houses.sort()
        coords = [p[0] for p in houses]
        ids = [p[1] for p in houses]
        parent = list(range(len(coords) + 1))
        cols[x] = (coords, parent, ids)
        for j, house_id in enumerate(ids):
            col_idx[house_id] = j

    def sweep(data, lo, hi, horizontal):
        coords, parent, ids = data
        left = bisect_left(coords, lo)
        right = bisect_right(coords, hi)
        pos = find(parent, left)
        found = 0

        while pos < right:
            house_id = ids[pos]

            if horizontal:
                other_coords, other_parent, _ = cols[xs[house_id]]
                other_pos = col_idx[house_id]
            else:
                other_coords, other_parent, _ = rows[ys[house_id]]
                other_pos = row_idx[house_id]

            parent[pos] = find(parent, pos + 1)
            other_parent[other_pos] = find(other_parent, other_pos + 1)

            found += 1
            pos = find(parent, pos)

        return found

    count = 0

    for _ in range(m):
        direction = next(it)
        length = int(next(it))

        if direction == b'L':
            nx = sx - length
            if sy in rows:
                count += sweep(rows[sy], nx, sx, True)
            sx = nx
        elif direction == b'R':
            nx = sx + length
            if sy in rows:
                count += sweep(rows[sy], sx, nx, True)
            sx = nx
        elif direction == b'D':
            ny = sy - length
            if sx in cols:
                count += sweep(cols[sx], ny, sy, False)
            sy = ny
        else:  # U
            ny = sy + length
            if sx in cols:
                count += sweep(cols[sx], sy, ny, False)
            sy = ny

    print(sx, sy, count)


if __name__ == "__main__":
    main()