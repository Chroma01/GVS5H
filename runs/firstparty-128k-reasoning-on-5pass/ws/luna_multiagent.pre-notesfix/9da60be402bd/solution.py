import sys
from collections import deque

def main():
    input = sys.stdin.readline
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    incoming = [[[] for _ in range(26)] for _ in range(n)]
    outgoing_mask = [[0] * 26 for _ in range(n)]

    odd_initial = []
    for i in range(n):
        for j, ch in enumerate(grid[i]):
            if ch != '-':
                k = ord(ch) - 97
                incoming[j][k].append(i)
                outgoing_mask[i][k] |= 1 << j
                odd_initial.append(i * n + j)

    def bfs(parity):
        total = n * n
        dist = [-1] * total
        visited_rows = [0] * n
        q = deque()

        if parity == 0:
            for i in range(n):
                idx = i * n + i
                dist[idx] = 0
                visited_rows[i] |= 1 << i
                q.append(idx)
        else:
            for idx in odd_initial:
                if dist[idx] == -1:
                    i, j = divmod(idx, n)
                    dist[idx] = 1
                    visited_rows[i] |= 1 << j
                    q.append(idx)

        while q:
            idx = q.popleft()
            x, y = divmod(idx, n)
            nd = dist[idx] + 2

            for c in range(26):
                predecessors = incoming[x][c]
                targets = outgoing_mask[y][c]
                if not predecessors or not targets:
                    continue

                for a in predecessors:
                    fresh = targets & ~visited_rows[a]
                    if not fresh:
                        continue

                    visited_rows[a] |= fresh
                    base = a * n
                    while fresh:
                        bit = fresh & -fresh
                        b = bit.bit_length() - 1
                        nxt = base + b
                        dist[nxt] = nd
                        q.append(nxt)
                        fresh ^= bit

        return dist

    even_dist = bfs(0)
    odd_dist = bfs(1)

    ans = []
    for i in range(n):
        row = []
        for j in range(n):
            idx = i * n + j
            e = even_dist[idx]
            o = odd_dist[idx]
            if e == -1:
                row.append(str(o))
            elif o == -1:
                row.append(str(e))
            else:
                row.append(str(min(e, o)))
        ans.append(" ".join(row))

    print("\n".join(ans))

if __name__ == "__main__":
    main()