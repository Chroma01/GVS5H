import sys
from collections import deque

def main():
    input = sys.stdin.readline
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    incoming = [[[ ] for _ in range(26)] for _ in range(n)]
    outgoing = [[[ ] for _ in range(26)] for _ in range(n)]
    out_mask = [[0] * 26 for _ in range(n)]

    for u in range(n):
        row = grid[u]
        for v, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                outgoing[u][c].append(v)
                incoming[v][c].append(u)
                out_mask[u][c] |= 1 << v

    total = n * n

    def bfs(parity):
        dist = [-1] * total
        seen_mask = [0] * n
        q = deque()

        if parity == 0:
            for i in range(n):
                state = i * n + i
                dist[state] = 0
                seen_mask[i] |= 1 << i
                q.append(state)
        else:
            for u in range(n):
                row = grid[u]
                base = u * n
                for v, ch in enumerate(row):
                    if ch != '-':
                        state = base + v
                        dist[state] = 1
                        seen_mask[u] |= 1 << v
                        q.append(state)

        while q:
            state = q.popleft()
            u = state // n
            v = state - u * n
            next_dist = dist[state] + 2

            for c in range(26):
                right_choices = out_mask[v][c]
                if right_choices == 0:
                    continue

                for p in incoming[u][c]:
                    new_vertices = right_choices & ~seen_mask[p]
                    if new_vertices == 0:
                        continue

                    seen_mask[p] |= new_vertices
                    base = p * n

                    while new_vertices:
                        bit = new_vertices & -new_vertices
                        qv = bit.bit_length() - 1
                        nxt = base + qv
                        dist[nxt] = next_dist
                        q.append(nxt)
                        new_vertices -= bit

        return dist

    even_dist = bfs(0)
    odd_dist = bfs(1)

    lines = []
    for i in range(n):
        row = []
        base = i * n
        for j in range(n):
            e = even_dist[base + j]
            o = odd_dist[base + j]
            if e == -1:
                ans = o
            elif o == -1:
                ans = e
            else:
                ans = min(e, o)
            row.append(str(ans))
        lines.append(" ".join(row))

    sys.stdout.write("\n".join(lines))

if __name__ == "__main__":
    main()