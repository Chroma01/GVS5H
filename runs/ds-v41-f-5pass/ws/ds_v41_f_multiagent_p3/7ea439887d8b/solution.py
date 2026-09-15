import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    x = int(data[idx]); idx += 1

    # nodes: 0..n-1  = (vertex v, original orientation)
    #        n..2n-1 = (vertex v, reversed orientation)
    adj = [[] for _ in range(2 * n)]
    for _ in range(m):
        u = int(data[idx]) - 1; idx += 1
        v = int(data[idx]) - 1; idx += 1
        # original layer keeps direction u -> v
        adj[u].append((v, 1))
        # reversed layer flips it: v -> u
        adj[n + v].append((n + u, 1))
    # reversing all edges toggles orientation at the current vertex
    for v in range(n):
        adj[v].append((n + v, x))
        adj[n + v].append((v, x))

    INF = float('inf')
    dist = [INF] * (2 * n)
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for nxt, w in adj[node]:
            nd = d + w
            if nd < dist[nxt]:
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))

    ans = dist[n - 1]
    if dist[2 * n - 1] < ans:
        ans = dist[2 * n - 1]
    sys.stdout.write(str(ans) + "\n")


main()