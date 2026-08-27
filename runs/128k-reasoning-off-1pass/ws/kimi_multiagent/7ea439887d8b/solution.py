import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1

    adj = [[] for _ in range(N + 1)]      # original edges
    radj = [[] for _ in range(N + 1)]     # reversed edges

    for _ in range(M):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        adj[u].append(v)
        radj[v].append(u)

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
        # move along an edge in current orientation
        nd = d + 1
        for to in (adj[v] if o == 0 else radj[v]):
            if nd < dist[o][to]:
                dist[o][to] = nd
                heapq.heappush(h, (nd, to, o))
        # reverse all edges
        nd = d + X
        no = o ^ 1
        if nd < dist[no][v]:
            dist[no][v] = nd
            heapq.heappush(h, (nd, v, no))

    ans = dist[0][N]
    if dist[1][N] < ans:
        ans = dist[1][N]
    sys.stdout.write(str(ans) + "\n")

main()