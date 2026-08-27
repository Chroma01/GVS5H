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
    dist = [[inf] * n for _ in range(2)]
    dist[0][0] = 0
    pq = [(0, 0, 0)]  # cost, vertex, parity

    while pq:
        d, v, parity = heapq.heappop(pq)
        if d != dist[parity][v]:
            continue

        opposite = parity ^ 1
        nd = d + x
        if nd < dist[opposite][v]:
            dist[opposite][v] = nd
            heapq.heappush(pq, (nd, v, opposite))

        edges = out_edges[v] if parity == 0 else in_edges[v]
        nd = d + 1
        current_dist = dist[parity]
        for to in edges:
            if nd < current_dist[to]:
                current_dist[to] = nd
                heapq.heappush(pq, (nd, to, parity))

    print(min(dist[0][n - 1], dist[1][n - 1]))

if __name__ == "__main__":
    solve()