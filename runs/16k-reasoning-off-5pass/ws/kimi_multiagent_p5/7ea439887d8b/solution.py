import sys
import heapq

def main():
    input = sys.stdin.readline
    N, M, X = map(int, input().split())
    out = [[] for _ in range(N + 1)]
    inn = [[] for _ in range(N + 1)]
    for _ in range(M):
        u, v = map(int, input().split())
        out[u].append(v)
        inn[v].append(u)

    INF = 1 << 62
    dist = [[INF, INF] for _ in range(N + 1)]
    dist[1][0] = 0
    pq = [(0, 1, 0)]  # (cost, vertex, parity)

    while pq:
        d, v, p = heapq.heappop(pq)
        if d > dist[v][p]:
            continue
        # flip parity at same vertex
        nd = d + X
        if nd < dist[v][p ^ 1]:
            dist[v][p ^ 1] = nd
            heapq.heappush(pq, (nd, v, p ^ 1))
        # move along edges
        adj = out[v] if p == 0 else inn[v]
        nd = d + 1
        for u in adj:
            if nd < dist[u][p]:
                dist[u][p] = nd
                heapq.heappush(pq, (nd, u, p))

    print(min(dist[N][0], dist[N][1]))

main()