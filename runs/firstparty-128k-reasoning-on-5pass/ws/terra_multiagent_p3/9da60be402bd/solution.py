import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    n = int(input())
    graph = [input().strip() for _ in range(n)]

    # incoming[v][c]: vertices u such that u -> v has label c
    incoming = [[[ ] for _ in range(26)] for _ in range(n)]
    # outgoing_mask[u][c]: bitmask of vertices v such that u -> v has label c
    outgoing_mask = [[0] * 26 for _ in range(n)]

    for u in range(n):
        row = graph[u]
        for v, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                incoming[v][c].append(u)
                outgoing_mask[u][c] |= 1 << v

    dist = [[-1] * n for _ in range(n)]
    full_mask = (1 << n) - 1
    unvisited = [full_mask] * n
    q = deque()

    # Empty palindrome centers.
    for i in range(n):
        dist[i][i] = 0
        unvisited[i] &= ~(1 << i)
        q.append(i * n + i)

    # One-edge palindrome centers.
    for u in range(n):
        for v, ch in enumerate(graph[u]):
            if ch != '-' and dist[u][v] == -1:
                dist[u][v] = 1
                unvisited[u] &= ~(1 << v)
                q.append(u * n + v)

    while q:
        state = q.popleft()
        u = state // n
        v = state % n
        nd = dist[u][v] + 2

        for c in range(26):
            predecessors = incoming[u][c]
            successors = outgoing_mask[v][c]

            if not predecessors or successors == 0:
                continue

            for x in predecessors:
                new_vertices = successors & unvisited[x]
                if new_vertices == 0:
                    continue

                unvisited[x] &= ~new_vertices

                while new_vertices:
                    lowbit = new_vertices & -new_vertices
                    y = lowbit.bit_length() - 1
                    dist[x][y] = nd
                    q.append(x * n + y)
                    new_vertices -= lowbit

    sys.stdout.write("\n".join(" ".join(map(str, row)) for row in dist))

if __name__ == "__main__":
    solve()