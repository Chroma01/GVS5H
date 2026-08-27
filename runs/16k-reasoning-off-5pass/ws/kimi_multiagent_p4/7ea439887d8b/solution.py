import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1

    out_adj = [[] for _ in range(N + 1)]
    in_adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        out_adj[u].append(v)
        in_adj[v].append(u)

    INF = 1 << 62
    # dist[parity][vertex]
    dist = [[INF] * (N + 1) for _ in range(2)]
    dist[0][1] = 0
    heap = [(0, 1, 0)]  # (distance, vertex, parity)

    while heap:
        d, v, p = heapq.heappop(heap)
        if d > dist[p][v]:
            continue
        # Move along edges (cost 1, parity unchanged)
        adj = out_adj[v] if p == 0 else in_adj[v]
        nd = d + 1
        for u in adj:
            if nd < dist[p][u]:
                dist[p][u] = nd
                heapq.heappush(heap, (nd, u, p))
        # Reverse all edges (cost X, flip parity, stay at same vertex)
        nd2 = d + X
        np_ = 1 - p
        if nd2 < dist[np_][v]:
            dist[np_][v] = nd2
            heapq.heappush(heap, (nd2, v, np_))

    ans = dist[0][N]
    if dist[1][N] < ans:
        ans = dist[1][N]
    sys.stdout.write(str(ans) + "\n")

main()