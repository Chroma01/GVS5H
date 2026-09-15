import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    m = int(data[pos]); pos += 1
    x = int(data[pos]); pos += 1

    total = 2 * n
    graph = [[] for _ in range(total)]

    for _ in range(m):
        u = int(data[pos]) - 1; pos += 1
        v = int(data[pos]) - 1; pos += 1
        # normal orientation: original edge u -> v, cost 1
        graph[u].append((v, 1))
        # reversed orientation: edge becomes v -> u, at states offset by n
        graph[v + n].append((u + n, 1))

    for v in range(n):
        # switch orientation at the same vertex, cost X (both directions)
        graph[v].append((v + n, x))
        graph[v + n].append((v, x))

    INF = float('inf')
    dist = [INF] * total
    dist[0] = 0
    pq = [(0, 0)]

    goal_normal = n - 1
    goal_reversed = 2 * n - 1

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == goal_normal or u == goal_reversed:
            sys.stdout.write(str(d) + "\n")
            return
        for w, c in graph[u]:
            nd = d + c
            if nd < dist[w]:
                dist[w] = nd
                heapq.heappush(pq, (nd, w))

    sys.stdout.write(str(min(dist[goal_normal], dist[goal_reversed])) + "\n")

main()