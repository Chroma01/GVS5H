import sys
from bisect import bisect_left
from collections import defaultdict

def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); M = int(data[p+1]); Sx = int(data[p+2]); Sy = int(data[p+3])
    p += 4
    X = [0]*N
    Y = [0]*N
    for i in range(N):
        X[i] = int(data[p]); Y[i] = int(data[p+1]); p += 2
    moves = []
    for i in range(M):
        moves.append((data[p].decode(), int(data[p+1]))); p += 2

    # Build row index: y -> sorted list of (x, idx); col index: x -> sorted list of (y, idx)
    rows = defaultdict(list)
    cols = defaultdict(list)
    for i in range(N):
        rows[Y[i]].append((X[i], i))
        cols[X[i]].append((Y[i], i))

    row_key = {}      # y -> sorted list of x
    row_id = {}       # y -> parallel list of house idx
    row_parent = {}   # y -> DSU successor parent array
    for y, lst in rows.items():
        lst.sort()
        row_key[y] = [a for a, _ in lst]
        row_id[y] = [b for _, b in lst]
        row_parent[y] = list(range(len(lst)+1))

    col_key = {}
    col_id = {}
    col_parent = {}
    for x, lst in cols.items():
        lst.sort()
        col_key[x] = [a for a, _ in lst]
        col_id[x] = [b for _, b in lst]
        col_parent[x] = list(range(len(lst)+1))

    # Position of each house in its row list and column list
    pos_row = [0]*N
    pos_col = [0]*N
    for y, ids in row_id.items():
        for j, idx in enumerate(ids):
            pos_row[idx] = j
    for x, ids in col_id.items():
        for j, idx in enumerate(ids):
            pos_col[idx] = j

    visited = bytearray(N)
    count = 0

    def find(parent, i):
        # iterative path compression
        root = i
        while parent[root] != root:
            root = parent[root]
        while parent[i] != root:
            parent[i], i = root, parent[i]
        return root

    x, y = Sx, Sy
    for d, c in moves:
        if d == 'U':
            nx, ny = x, y + c
        elif d == 'D':
            nx, ny = x, y - c
        elif d == 'L':
            nx, ny = x - c, y
        else:  # 'R'
            nx, ny = x + c, y

        if y == ny:  # horizontal move
            lo = x if x < nx else nx
            hi = nx if x < nx else x
            if y in row_key:
                keys = row_key[y]
                ids = row_id[y]
                parent = row_parent[y]
                l = bisect_left(keys, lo)
                j = find(parent, l)
                L = len(keys)
                while j < L and keys[j] <= hi:
                    idx = ids[j]
                    if not visited[idx]:
                        visited[idx] = 1
                        count += 1
                        # remove from column structure too
                        cp = col_parent[X[idx]]
                        pj = pos_col[idx]
                        cp[pj] = find(cp, pj + 1)
                    parent[j] = find(parent, j + 1)
                    j = find(parent, j)
        else:  # vertical move
            lo = y if y < ny else ny
            hi = ny if y < ny else y
            if x in col_key:
                keys = col_key[x]
                ids = col_id[x]
                parent = col_parent[x]
                l = bisect_left(keys, lo)
                j = find(parent, l)
                L = len(keys)
                while j < L and keys[j] <= hi:
                    idx = ids[j]
                    if not visited[idx]:
                        visited[idx] = 1
                        count += 1
                        # remove from row structure too
                        rp = row_parent[Y[idx]]
                        pj = pos_row[idx]
                        rp[pj] = find(rp, pj + 1)
                    parent[j] = find(parent, j + 1)
                    j = find(parent, j)

        x, y = nx, ny

    sys.stdout.write(f"{x} {y} {count}\n")

main()