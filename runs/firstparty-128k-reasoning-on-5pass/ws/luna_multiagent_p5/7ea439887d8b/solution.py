import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline
    n, m, x = map(int, input().split())

    graph = [[] for _ in range(n)]
    reverse_graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        reverse_graph[v].append(u)

    inf = 10**30
    dist = [[inf] * n for _ in range(2)]
    dist[0][0] = 0

    pq = [(0, 0, 0)]  # cost, vertex, parity

    while pq:
        cost, v, parity = heapq.heappop(pq)
        if cost != dist[parity][v]:
            continue

        if v == n - 1:
            print(cost)
            return

        next_graph = graph if parity == 0 else reverse_graph

        for to in next_graph[v]:
            new_cost = cost + 1
            if new_cost < dist[parity][to]:
                dist[parity][to] = new_cost
                heapq.heappush(pq, (new_cost, to, parity))

        new_parity = parity ^ 1
        new_cost = cost + x
        if new_cost < dist[new_parity][v]:
            dist[new_parity][v] = new_cost
            heapq.heappush(pq, (new_cost, v, new_parity))


if __name__ == "__main__":
    solve()