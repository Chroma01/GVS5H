import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); M = int(data[p+1]); Sx = int(data[p+2]); Sy = int(data[p+3])
    p += 4

    by_y = {}
    by_x = {}
    for i in range(N):
        x = int(data[p]); y = int(data[p+1]); p += 2
        by_y.setdefault(y, []).append((x, i))
        by_x.setdefault(x, []).append((y, i))

    # For each horizontal line y = const: sorted x-coords of houses on it.
    # For each vertical line x = const: sorted y-coords of houses on it.
    # Each line also gets a DSU "successor" array so that once a house has
    # been counted it is skipped in O(alpha) on later sweeps of the same line.
    line_coords = {}   # key -> sorted list of the varying coordinate
    line_parent = {}   # key -> DSU parent array (len+1, sentinel = len)

    for y, lst in by_y.items():
        lst.sort()
        line_coords[('y', y)] = [c for c, _ in lst]
        line_parent[('y', y)] = list(range(len(lst) + 1))
    for x, lst in by_x.items():
        lst.sort()
        line_coords[('x', x)] = [c for c, _ in lst]
        line_parent[('x', x)] = list(range(len(lst) + 1))

    def find(parent, k):
        # iterative with path compression; returns smallest unvisited index >= k
        root = k
        while parent[root] != root:
            root = parent[root]
        while parent[k] != root:
            parent[k], k = root, parent[k]
        return root

    visited_count = 0

    def sweep(key, lo, hi):
        # Count (and mark) all not-yet-counted houses on `key`'s line whose
        # varying coordinate lies in [lo, hi] (inclusive both ends).
        nonlocal visited_count
        coords = line_coords.get(key)
        if coords is None:
            return
        parent = line_parent[key]
        l = bisect_left(coords, lo)
        r = bisect_right(coords, hi)  # exclusive bound
        k = find(parent, l)
        while k < r:
            visited_count += 1
            parent[k] = k + 1          # remove house k forever
            k = find(parent, k + 1)

    x, y = Sx, Sy
    for _ in range(M):
        d = data[p]; c = int(data[p+1]); p += 2
        if d == b'U':
            ny = y + c
            sweep(('x', x), y, ny)
            y = ny
        elif d == b'D':
            ny = y - c
            sweep(('x', x), ny, y)
            y = ny
        elif d == b'L':
            nx = x - c
            sweep(('y', y), nx, x)
            x = nx
        else:  # b'R'
            nx = x + c
            sweep(('y', y), x, nx)
            x = nx

    sys.stdout.write(f"{x} {y} {visited_count}\n")

main()