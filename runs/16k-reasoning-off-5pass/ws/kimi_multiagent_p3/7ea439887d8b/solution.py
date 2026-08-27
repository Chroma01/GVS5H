import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1

    out_edges = [[] for _ in range(N + 1)]
    in_edges = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        out_edges[u].append(v)
        in_edges[v].append(u)

    INF = float('inf')
    # dist[parity][vertex]
    dist = [[INF] * (N + 1) for _ in range(2)]
    dist[0][1] = 0
    heap = [(0, 1, 0)]  # (cost, vertex, parity)

    while heap:
        d, v, p = heapq.heappop(heap)
        if d > dist[p][v]:
            continue
        # Move along edges in current orientation
        adj = out_edges[v] if p == 0 else in_edges[v]
        nd = d + 1
        for u in adj:
            if nd < dist[p][u]:
                dist[p][u] = nd
                heapq.heappush(heap, (nd, u, p))
        # Flip orientation at same vertex
        nd = d + X
        q = p ^ 1
        if nd < dist[q][v]:
            dist[q][v] = nd
            heapq.heappush(heap, (nd, v, q))

    print(min(dist[0][N], dist[1][N]))

main()