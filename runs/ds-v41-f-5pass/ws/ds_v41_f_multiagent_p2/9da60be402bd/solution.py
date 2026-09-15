import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    grid = data[1:1 + n]

    # Per-label masks.  in_mask[c][v] = bitset of x with edge x -> v label c
    #                    out_mask[c][u] = bitset of y with edge u -> y label c
    in_mask = [[0] * n for _ in range(26)]
    out_mask = [[0] * n for _ in range(26)]
    for i in range(n):
        row = grid[i]
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                out_mask[c][i] |= (1 << j)
                in_mask[c][j] |= (1 << i)

    # Precompute the non-empty incoming labels for each vertex.
    in_labels = [[] for _ in range(n)]
    for u in range(n):
        lst = in_labels[u]
        for c in range(26):
            if in_mask[c][u]:
                lst.append((c, in_mask[c][u]))

    dist = [[-1] * n for _ in range(n)]
    unvis = [(1 << n) - 1 for _ in range(n)]  # unvis[x] = unvisited columns in row x
    q = deque()

    # Base case: empty palindrome, length 0.
    for i in range(n):
        dist[i][i] = 0
        unvis[i] &= ~(1 << i)
        q.append((i, i, 0))

    # Base case: single edge, length 1.
    for i in range(n):
        row = grid[i]
        for j in range(n):
            if row[j] != '-' and dist[i][j] == -1:
                dist[i][j] = 1
                unvis[i] &= ~(1 << j)
                q.append((i, j, 1))

    # BFS on pair states (u, v): shortest palindromic walk u -> v.
    while q:
        u, v, d = q.popleft()
        nd = d + 2
        for c, A in in_labels[u]:
            B = out_mask[c][v]
            if not B:
                continue
            a = A
            while a:
                xb = a & (-a)
                x = xb.bit_length() - 1
                a ^= xb
                cand = B & unvis[x]
                while cand:
                    yb = cand & (-cand)
                    cand ^= yb
                    y = yb.bit_length() - 1
                    unvis[x] &= ~yb
                    dist[x][y] = nd
                    q.append((x, y, nd))

    out_lines = [' '.join(map(str, dist[i])) for i in range(n)]
    sys.stdout.write('\n'.join(out_lines) + '\n')


main()