import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    x = int(data[idx]); idx += 1

    size = 2 * n
    # Node indexing: vertex v in normal layer -> v
    #                vertex v in reversed layer -> n + v
    adj = [[] for _ in range(size)]

    for _ in range(m):
        u = int(data[idx]) - 1; idx += 1
        v = int(data[idx]) - 1; idx += 1
        # normal orientation: u -> v
        adj[u].append((v, 1))
        # reversed orientation: v -> u
        adj[n + v].append((n + u, 1))

    # Flip edges between layers at the same vertex, cost X
    for v in range(n):
        adj[v].append((n + v, x))
        adj[n + v].append((v, x))

    INF = float('inf')
    dist = [INF] * size
    dist[0] = 0
    pq = [(0, 0)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for w, c in adj[u]:
            nd = d + c
            if nd < dist[w]:
                dist[w] = nd
                heapq.heappush(pq, (nd, w))

    ans = min(dist[n - 1], dist[2 * n - 1])
    sys.stdout.write(str(ans) + "\n")


main()