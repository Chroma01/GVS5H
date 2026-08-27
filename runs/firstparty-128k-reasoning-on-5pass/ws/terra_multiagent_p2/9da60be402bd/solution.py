import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    n = int(input())
    graph = [input().strip() for _ in range(n)]

    incoming = [[[] for _ in range(n)] for _ in range(26)]
    outgoing = [[[] for _ in range(n)] for _ in range(26)]

    dist = [-1] * (n * n)
    q = deque()
    remaining = n * n

    # Empty palindrome centers.
    for i in range(n):
        state = i * n + i
        dist[state] = 0
        q.append(state)
        remaining -= 1

    # One-edge palindrome centers.
    for i in range(n):
        row = graph[i]
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                outgoing[c][i].append(j)
                incoming[c][j].append(i)

                state = i * n + j
                if dist[state] == -1:
                    dist[state] = 1
                    q.append(state)
                    remaining -= 1

    # From inner endpoints (u, v), add matching edges x->u and v->y.
    while q and remaining:
        state = q.popleft()
        u = state // n
        v = state - u * n
        nd = dist[state] + 2

        for c in range(26):
            lefts = incoming[c][u]
            rights = outgoing[c][v]
            if not lefts or not rights:
                continue

            for x in lefts:
                base = x * n
                for y in rights:
                    nxt = base + y
                    if dist[nxt] == -1:
                        dist[nxt] = nd
                        q.append(nxt)
                        remaining -= 1

    out = []
    for i in range(n):
        out.append(" ".join(map(str, dist[i * n:(i + 1) * n])))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()