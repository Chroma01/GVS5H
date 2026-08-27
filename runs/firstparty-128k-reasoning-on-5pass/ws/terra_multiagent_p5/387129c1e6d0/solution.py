import sys
from bisect import bisect_left

def solve():
    input = sys.stdin.readline

    N, M, sx, sy = map(int, input().split())

    xs = [0] * N
    ys = [0] * N

    rows = {}
    cols = {}

    for i in range(N):
        x, y = map(int, input().split())
        xs[i] = x
        ys[i] = y
        rows.setdefault(y, []).append(i)
        cols.setdefault(x, []).append(i)

    sentinel = N
    row_parent = list(range(N + 1))
    col_parent = list(range(N + 1))
    row_next = [sentinel] * N
    col_next = [sentinel] * N

    # Each row stores (sorted x-coordinates, corresponding house IDs).
    for y, ids in rows.items():
        ids.sort(key=xs.__getitem__)
        values = [xs[i] for i in ids]
        rows[y] = (values, ids)
        for j in range(len(ids) - 1):
            row_next[ids[j]] = ids[j + 1]

    # Each column stores (sorted y-coordinates, corresponding house IDs).
    for x, ids in cols.items():
        ids.sort(key=ys.__getitem__)
        values = [ys[i] for i in ids]
        cols[x] = (values, ids)
        for j in range(len(ids) - 1):
            col_next[ids[j]] = ids[j + 1]

    def find(parent, v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    answer = 0
    x, y = sx, sy

    for _ in range(M):
        d, c_str = input().split()
        c = int(c_str)

        if d == 'L':
            nx, ny = x - c, y
        elif d == 'R':
            nx, ny = x + c, y
        elif d == 'D':
            nx, ny = x, y - c
        else:
            nx, ny = x, y + c

        if y == ny:
            data = rows.get(y)
            if data is not None:
                values, ids = data
                lo, hi = (x, nx) if x <= nx else (nx, x)
                pos = bisect_left(values, lo)

                if pos < len(ids):
                    house = find(row_parent, ids[pos])
                    while house != sentinel and xs[house] <= hi:
                        row_parent[house] = find(row_parent, row_next[house])
                        col_parent[house] = find(col_parent, col_next[house])
                        answer += 1
                        house = find(row_parent, house)
        else:
            data = cols.get(x)
            if data is not None:
                values, ids = data
                lo, hi = (y, ny) if y <= ny else (ny, y)
                pos = bisect_left(values, lo)

                if pos < len(ids):
                    house = find(col_parent, ids[pos])
                    while house != sentinel and ys[house] <= hi:
                        row_parent[house] = find(row_parent, row_next[house])
                        col_parent[house] = find(col_parent, col_next[house])
                        answer += 1
                        house = find(col_parent, house)

        x, y = nx, ny

    print(x, y, answer)

if __name__ == "__main__":
    solve()