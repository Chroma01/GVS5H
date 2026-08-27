import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = int(next(it))

    out_adj = [[] for _ in range(N + 1)]  # original edges
    in_adj = [[] for _ in range(N + 1)]   # reversed edges

    for _ in range(M):
        u = int(next(it))
        v = int(next(it))
        out_adj[u].append(v)
        in_adj[v].append(u)

    INF = 1 << 62
    # dist[orientation][vertex]
    dist = [[INF] * (N + 1) for _ in range(2)]
    dist[0][1] = 0

    # heap entries: (cost, vertex, orientation)
    h = [(0, 1, 0)]

    while h:
        d, v, o = heapq.heappop(h)
        if d != dist[o][v]:
            continue
        # Move along an edge with cost 1
        adj = out_adj[v] if o == 0 else in_adj[v]
        nd = d + 1
        for u in adj:
            if nd < dist[o][u]:
                dist[o][u] = nd
                heapq.heappush(h, (nd, u, o))
        # Reverse all edges with cost X
        nd = d + X
        no = o ^ 1
        if nd < dist[no][v]:
            dist[no][v] = nd
            heapq.heappush(h, (nd, v, no))

    ans = dist[0][N]
    if dist[1][N] < ans:
        ans = dist[1][N]
    print(ans)

main()