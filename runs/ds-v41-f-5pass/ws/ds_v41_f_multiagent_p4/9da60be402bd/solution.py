import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    grid = data[1:1+N]
    
    outmask = [[0]*26 for _ in range(N)]
    inlist = [[[] for _ in range(N)] for _ in range(26)]
    vchars = [[] for _ in range(N)]
    
    for u in range(N):
        row = grid[u]
        for v, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                outmask[u][c] |= (1 << v)
                inlist[c][v].append(u)
    for u in range(N):
        for c in range(26):
            if outmask[u][c]:
                vchars[u].append(c)
    
    dist = [[-1]*N for _ in range(N)]
    unsettled = [(1 << N) - 1] * N
    q = deque()
    
    # level 0: empty palindromes
    for i in range(N):
        dist[i][i] = 0
        unsettled[i] &= ~(1 << i)
        q.append((i, i))
    
    # level 1: single edges (u != v). Self-loops are skipped as base states,
    # but remain available as edges in extensions.
    for u in range(N):
        row = grid[u]
        for v, ch in enumerate(row):
            if ch != '-' and u != v:
                if dist[u][v] == -1:
                    dist[u][v] = 1
                    unsettled[u] &= ~(1 << v)
                    q.append((u, v))
    
    while q:
        x, y = q.popleft()
        d = dist[x][y]
        nd = d + 2
        newacc = [0] * N
        for c in vchars[y]:
            mask = outmask[y][c]
            for a in inlist[c][x]:
                newacc[a] |= mask
        for a in range(N):
            mask = newacc[a]
            if mask:
                newbits = mask & unsettled[a]
                if newbits:
                    m = newbits
                    while m:
                        lsb = m & -m
                        b = lsb.bit_length() - 1
                        dist[a][b] = nd
                        unsettled[a] &= ~lsb
                        q.append((a, b))
                        m ^= lsb
    
    out_lines = []
    for i in range(N):
        out_lines.append(' '.join(str(dist[i][j]) for j in range(N)))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()