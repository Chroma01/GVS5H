import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, x = data[0], data[1], data[2]
    outgoing = [[] for _ in range(n)]
    incoming = [[] for _ in range(n)]

    pos = 3
    for _ in range(m):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        outgoing[u].append(v)
        incoming[v].append(u)

    inf = 10**30
    dist = [inf] * (2 * n)
    dist[0] = 0
    heap = [(0, 0)]

    while heap:
        d, state = heapq.heappop(heap)
        if d != dist[state]:
            continue

        vertex = state % n
        parity = state // n

        if vertex == n - 1:
            print(d)
            return

        other = (1 - parity) * n + vertex
        nd = d + x
        if nd < dist[other]:
            dist[other] = nd
            heapq.heappush(heap, (nd, other))

        neighbors = outgoing[vertex] if parity == 0 else incoming[vertex]
        for nxt in neighbors:
            next_state = parity * n + nxt
            nd = d + 1
            if nd < dist[next_state]:
                dist[next_state] = nd
                heapq.heappush(heap, (nd, next_state))


if __name__ == "__main__":
    solve()