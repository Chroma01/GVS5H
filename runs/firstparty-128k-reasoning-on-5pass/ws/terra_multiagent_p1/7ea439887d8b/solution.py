import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline
    n, m, x = map(int, input().split())

    out_edges = [[] for _ in range(n)]
    in_edges = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        out_edges[u].append(v)
        in_edges[v].append(u)

    inf = 10**30
    dist = [inf] * (2 * n)
    dist[0] = 0  # vertex 0, original orientation

    pq = [(0, 0)]

    while pq:
        d, state = heapq.heappop(pq)
        if d != dist[state]:
            continue

        v = state % n
        orientation = state // n

        if orientation == 0:
            neighbors = out_edges[v]
        else:
            neighbors = in_edges[v]

        nd = d + 1
        base = orientation * n
        for to in neighbors:
            nxt = base + to
            if nd < dist[nxt]:
                dist[nxt] = nd
                heapq.heappush(pq, (nd, nxt))

        toggled = (1 - orientation) * n + v
        nd = d + x
        if nd < dist[toggled]:
            dist[toggled] = nd
            heapq.heappush(pq, (nd, toggled))

    print(min(dist[n - 1], dist[2 * n - 1]))


if __name__ == "__main__":
    solve()