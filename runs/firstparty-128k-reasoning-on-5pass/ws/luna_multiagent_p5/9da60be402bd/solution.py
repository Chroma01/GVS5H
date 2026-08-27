import sys
import heapq


def solve():
    input = sys.stdin.readline
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    # pred[u][c] = vertices x such that x -> u has label c
    pred = [[[] for _ in range(26)] for _ in range(n)]
    # outmask[v][c] = bitmask of vertices y such that v -> y has label c
    outmask = [[0] * 26 for _ in range(n)]

    for i in range(n):
        for j, ch in enumerate(grid[i]):
            if ch != '-':
                c = ord(ch) - 97
                pred[j][c].append(i)
                outmask[i][c] |= 1 << j

    inf = 10**9
    dist = [[inf] * n for _ in range(n)]
    pq = []

    # Empty paths.
    for i in range(n):
        dist[i][i] = 0
        heapq.heappush(pq, (0, i * n + i))

    # One-edge paths.
    for i in range(n):
        for j, ch in enumerate(grid[i]):
            if ch != '-' and dist[i][j] > 1:
                dist[i][j] = 1
                heapq.heappush(pq, (1, i * n + j))

    # Unassigned pair states. A state is removed when its shortest distance
    # is first discovered; Dijkstra order guarantees that this is optimal.
    all_bits = (1 << n) - 1
    unassigned = []
    for i in range(n):
        bits = all_bits
        for j in range(n):
            if dist[i][j] != inf:
                bits &= ~(1 << j)
        unassigned.append(bits)

    while pq:
        d, code = heapq.heappop(pq)
        u, v = divmod(code, n)
        if dist[u][v] != d:
            continue

        nd = d + 2

        # Add matching outer edges x -> u and v -> y.
        for c in range(26):
            targets = outmask[v][c]
            if not targets:
                continue

            for x in pred[u][c]:
                bits = unassigned[x] & targets
                while bits:
                    bit = bits & -bits
                    y = bit.bit_length() - 1
                    bits ^= bit
                    unassigned[x] ^= bit
                    dist[x][y] = nd
                    heapq.heappush(pq, (nd, x * n + y))

    out = []
    for row in dist:
        out.append(' '.join(str(x if x < inf else -1) for x in row))
    sys.stdout.write('\n'.join(out))


if __name__ == "__main__":
    solve()