import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, x = data[0], data[1], data[2]
    size = 2 * n
    graph = [[] for _ in range(size)]

    index = 3
    for _ in range(m):
        u = data[index] - 1
        v = data[index + 1] - 1
        index += 2

        # Orientation parity 0: original direction u -> v.
        graph[u].append((v, 1))

        # Orientation parity 1: reversed direction v -> u.
        graph[n + v].append((n + u, 1))

    # Reversing toggles the orientation parity and keeps the vertex.
    for v in range(n):
        graph[v].append((n + v, x))
        graph[n + v].append((v, x))

    inf = 10**30
    dist = [inf] * size
    dist[0] = 0
    heap = [(0, 0)]

    while heap:
        cost, state = heapq.heappop(heap)
        if cost != dist[state]:
            continue

        vertex = state % n
        if vertex == n - 1:
            print(cost)
            return

        for nxt, weight in graph[state]:
            new_cost = cost + weight
            if new_cost < dist[nxt]:
                dist[nxt] = new_cost
                heapq.heappush(heap, (new_cost, nxt))


if __name__ == "__main__":
    solve()