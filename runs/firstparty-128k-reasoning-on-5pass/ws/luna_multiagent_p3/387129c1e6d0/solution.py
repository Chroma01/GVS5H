import sys
from bisect import bisect_left, bisect_right


def find(parent, i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    sx = int(next(it))
    sy = int(next(it))

    house_x = [0] * n
    house_y = [0] * n

    groups_x_raw = {}
    groups_y_raw = {}

    for i in range(n):
        x = int(next(it))
        y = int(next(it))
        house_x[i] = x
        house_y[i] = y
        groups_x_raw.setdefault(x, []).append((y, i))
        groups_y_raw.setdefault(y, []).append((x, i))

    groups_x = {}
    pos_x = [0] * n
    for fixed_x, arr in groups_x_raw.items():
        arr.sort()
        values = [v for v, _ in arr]
        ids = [idx for _, idx in arr]
        parent = list(range(len(arr) + 1))
        groups_x[fixed_x] = (values, ids, parent)
        for pos, idx in enumerate(ids):
            pos_x[idx] = pos

    groups_y = {}
    pos_y = [0] * n
    for fixed_y, arr in groups_y_raw.items():
        arr.sort()
        values = [v for v, _ in arr]
        ids = [idx for _, idx in arr]
        parent = list(range(len(arr) + 1))
        groups_y[fixed_y] = (values, ids, parent)
        for pos, idx in enumerate(ids):
            pos_y[idx] = pos

    x, y = sx, sy
    visited_count = 0

    for _ in range(m):
        direction = next(it)
        length = int(next(it))

        if direction == b'U':
            new_y = y + length
            low, high = y, new_y
            record = groups_x.get(x)
            if record is not None:
                values, ids, parent = record
                left = bisect_left(values, low)
                right = bisect_right(values, high)
                pos = find(parent, left)
                while pos < right:
                    house_id = ids[pos]
                    visited_count += 1

                    parent[pos] = find(parent, pos + 1)

                    other_values, other_ids, other_parent = groups_y[house_y[house_id]]
                    other_pos = pos_y[house_id]
                    other_parent[other_pos] = find(other_parent, other_pos + 1)

                    pos = find(parent, pos)
            y = new_y

        elif direction == b'D':
            new_y = y - length
            low, high = new_y, y
            record = groups_x.get(x)
            if record is not None:
                values, ids, parent = record
                left = bisect_left(values, low)
                right = bisect_right(values, high)
                pos = find(parent, left)
                while pos < right:
                    house_id = ids[pos]
                    visited_count += 1

                    parent[pos] = find(parent, pos + 1)

                    other_values, other_ids, other_parent = groups_y[house_y[house_id]]
                    other_pos = pos_y[house_id]
                    other_parent[other_pos] = find(other_parent, other_pos + 1)

                    pos = find(parent, pos)
            y = new_y

        elif direction == b'R':
            new_x = x + length
            low, high = x, new_x
            record = groups_y.get(y)
            if record is not None:
                values, ids, parent = record
                left = bisect_left(values, low)
                right = bisect_right(values, high)
                pos = find(parent, left)
                while pos < right:
                    house_id = ids[pos]
                    visited_count += 1

                    parent[pos] = find(parent, pos + 1)

                    other_values, other_ids, other_parent = groups_x[house_x[house_id]]
                    other_pos = pos_x[house_id]
                    other_parent[other_pos] = find(other_parent, other_pos + 1)

                    pos = find(parent, pos)
            x = new_x

        else:  # direction == b'L'
            new_x = x - length
            low, high = new_x, x
            record = groups_y.get(y)
            if record is not None:
                values, ids, parent = record
                left = bisect_left(values, low)
                right = bisect_right(values, high)
                pos = find(parent, left)
                while pos < right:
                    house_id = ids[pos]
                    visited_count += 1

                    parent[pos] = find(parent, pos + 1)

                    other_values, other_ids, other_parent = groups_x[house_x[house_id]]
                    other_pos = pos_x[house_id]
                    other_parent[other_pos] = find(other_parent, other_pos + 1)

                    pos = find(parent, pos)
            x = new_x

    print(x, y, visited_count)


if __name__ == "__main__":
    main()