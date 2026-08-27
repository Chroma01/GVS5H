import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline
    n, m, x = map(int, input().split())

    forward = [[] for _ in range(n)]
    reverse = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        forward[u].append(v)
        reverse[v].append(u)

    inf = 10**30
    dist = [inf] * (2 * n)
    dist[0] = 0  # vertex 1, original orientation

    heap = [(0, 0)]

    while heap:
        cost, state = heapq.heappop(heap)
        if cost != dist[state]:
            continue

        parity = state // n
        vertex = state % n

        if vertex == n - 1:
            # This is not necessarily globally optimal until both states are
            # considered, so continue processing.
            pass

        # Reverse all edges.
        next_state = (parity ^ 1) * n + vertex
        next_cost = cost + x
        if next_cost < dist[next_state]:
            dist[next_state] = next_cost
            heapq.heappush(heap, (next_cost, next_state))

        # Move along an edge in the current orientation.
        adjacency = forward if parity == 0 else reverse
        for nxt in adjacency[vertex]:
            next_state = parity * n + nxt
            next_cost = cost + 1
            if next_cost < dist[next_state]:
                dist[next_state] = next_cost
                heapq.heappush(heap, (next_cost, next_state))

    print(min(dist[n - 1], dist[2 * n - 1]))


if __name__ == "__main__":
    solve()