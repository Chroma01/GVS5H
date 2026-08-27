import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); M = int(data[p+1]); Sx = int(data[p+2]); Sy = int(data[p+3])
    p += 4

    xs = [0]*N
    ys = [0]*N
    for i in range(N):
        xs[i] = int(data[p]); ys[i] = int(data[p+1]); p += 2

    moves = []
    for i in range(M):
        moves.append((data[p].decode(), int(data[p+1]))); p += 2

    # Group houses by row (y) for horizontal moves, and by column (x) for vertical moves.
    # Each group: sorted list of varying coordinates, parallel list of house indices,
    # and a DSU "next unvisited" parent array for O(alpha) skipping of visited houses.
    from collections import defaultdict
    rows = defaultdict(list)   # y -> list of (x, idx)
    cols = defaultdict(list)   # x -> list of (y, idx)
    for i in range(N):
        rows[ys[i]].append((xs[i], i))
        cols[xs[i]].append((ys[i], i))

    row_keys = {}
    row_idx = {}
    row_parent = {}
    for y, lst in rows.items():
        lst.sort()
        row_keys[y] = [v for v, _ in lst]
        row_idx[y] = [i for _, i in lst]
        row_parent[y] = list(range(len(lst) + 1))

    col_keys = {}
    col_idx = {}
    col_parent = {}
    for x, lst in cols.items():
        lst.sort()
        col_keys[x] = [v for v, _ in lst]
        col_idx[x] = [i for _, i in lst]
        col_parent[x] = list(range(len(lst) + 1))

    sys.setrecursionlimit(1 << 25)

    def find(parent, i):
        # iterative path compression
        root = i
        while parent[root] != root:
            root = parent[root]
        while parent[i] != root:
            parent[i], i = root, parent[i]
        return root

    visited_count = 0
    x, y = Sx, Sy

    for d, c in moves:
        if d == 'L' or d == 'R':
            nx = x - c if d == 'L' else x + c
            lo, hi = (nx, x) if nx < x else (x, nx)
            lst = row_keys.get(y)
            if lst is not None:
                parent = row_parent[y]
                idxs = row_idx[y]
                l = bisect_left(lst, lo)
                r = bisect_right(lst, hi)
                j = find(parent, l)
                while j < r:
                    visited_count += 1
                    parent[j] = j + 1
                    j = find(parent, j + 1)
            x = nx
        else:
            ny = y + c if d == 'U' else y - c
            lo, hi = (ny, y) if ny < y else (y, ny)
            lst = col_keys.get(x)
            if lst is not None:
                parent = col_parent[x]
                idxs = col_idx[x]
                l = bisect_left(lst, lo)
                r = bisect_right(lst, hi)
                j = find(parent, l)
                while j < r:
                    visited_count += 1
                    parent[j] = j + 1
                    j = find(parent, j + 1)
            y = ny

    sys.stdout.write(f"{x} {y} {visited_count}\n")

main()