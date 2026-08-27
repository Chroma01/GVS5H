import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1

    adj = [[] for _ in range(N + 1)]   # original orientation
    radj = [[] for _ in range(N + 1)]  # reversed orientation
    for _ in range(M):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        adj[u].append(v)
        radj[v].append(u)

    INF = 1 << 62
    # dist[p][v]: parity p = 0 original, 1 reversed
    dist = [[INF] * (N + 1) for _ in range(2)]
    dist[0][1] = 0
    pq = [(0, 1, 0)]  # (distance, vertex, parity)

    while pq:
        d, v, p = heapq.heappop(pq)
        if d > dist[p][v]:
            continue
        # Flip all edges: stay at v, toggle parity, cost X
        nd = d + X
        if nd < dist[p ^ 1][v]:
            dist[p ^ 1][v] = nd
            heapq.heappush(pq, (nd, v, p ^ 1))
        # Move along an edge in current orientation, cost 1
        nd = d + 1
        for u in (adj[v] if p == 0 else radj[v]):
            if nd < dist[p][u]:
                dist[p][u] = nd
                heapq.heappush(pq, (nd, u, p))

    ans = dist[0][N]
    if dist[1][N] < ans:
        ans = dist[1][N]
    sys.stdout.write(str(ans) + "\n")

main()