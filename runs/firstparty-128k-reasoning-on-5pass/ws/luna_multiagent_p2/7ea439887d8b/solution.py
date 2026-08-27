import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, x = data[0], data[1], data[2]
    outgoing = [[] for _ in range(n)]
    incoming = [[] for _ in range(n)]

    index = 3
    for _ in range(m):
        u = data[index] - 1
        v = data[index + 1] - 1
        index += 2
        outgoing[u].append(v)
        incoming[v].append(u)

    inf = 10**30
    dist = [inf] * (2 * n)
    dist[0] = 0  # (vertex 0, even reversal parity)
    heap = [(0, 0)]

    while heap:
        distance, state = heapq.heappop(heap)
        if distance != dist[state]:
            continue

        parity = state // n
        vertex = state % n

        if vertex == n - 1:
            print(distance)
            return

        neighbors = outgoing[vertex] if parity == 0 else incoming[vertex]

        for next_vertex in neighbors:
            next_state = parity * n + next_vertex
            next_distance = distance + 1
            if next_distance < dist[next_state]:
                dist[next_state] = next_distance
                heapq.heappush(heap, (next_distance, next_state))

        if parity == 0:
            next_state = state + n
        else:
            next_state = state - n

        next_distance = distance + x
        if next_distance < dist[next_state]:
            dist[next_state] = next_distance
            heapq.heappush(heap, (next_distance, next_state))


if __name__ == "__main__":
    solve()