import sys
from collections import deque

def main():
    input = sys.stdin.readline
    N = int(input())
    grid = [input().strip() for _ in range(N)]

    # in_edges[u] = list of (x, c) meaning edge x -> u labeled c
    in_edges = [[] for _ in range(N)]
    # out_by_letter[v][c] = list of y meaning edge v -> y labeled c
    out_by_letter = [[[] for _ in range(26)] for _ in range(N)]

    for i in range(N):
        row = grid[i]
        for j in range(N):
            ch = row[j]
            if ch != '-':
                c = ord(ch) - 97
                in_edges[j].append((i, c))
                out_by_letter[i][c].append(j)

    size = N * N
    dist = [-1] * size
    dq = deque()
    visited = 0

    # Distance-0 sources: (i, i) — empty palindrome
    for i in range(N):
        s = i * N + i
        dist[s] = 0
        dq.append(s)
        visited += 1

    # Distance-1 sources: (i, j) with an edge i -> j — single-char palindrome
    for i in range(N):
        row = grid[i]
        base = i * N
        for j in range(N):
            if row[j] != '-':
                s = base + j
                if dist[s] < 0:
                    dist[s] = 1
                    dq.append(s)
                    visited += 1

    # BFS: all transitions add exactly 2, and all dist-0 sources are enqueued
    # before dist-1 sources, so the queue stays non-decreasing in distance.
    while dq and visited < size:
        s = dq.popleft()
        u, v = divmod(s, N)
        nd = dist[s] + 2
        obv = out_by_letter[v]
        for x, c in in_edges[u]:
            for y in obv[c]:
                t = x * N + y
                if dist[t] < 0:
                    dist[t] = nd
                    dq.append(t)
                    visited += 1

    out_lines = []
    for i in range(N):
        base = i * N
        out_lines.append(' '.join(str(dist[base + j]) for j in range(N)))
    sys.stdout.write('\n'.join(out_lines) + '\n')

main()