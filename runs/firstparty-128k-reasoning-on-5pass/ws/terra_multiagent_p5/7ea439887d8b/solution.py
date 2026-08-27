import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, x = data[0], data[1], data[2]

    outgoing = [[] for _ in range(n)]
    incoming = [[] for _ in range(n)]

    p = 3
    for _ in range(m):
        u = data[p] - 1
        v = data[p + 1] - 1
        p += 2
        outgoing[u].append(v)
        incoming[v].append(u)

    inf = 10**30
    dist = [inf] * (2 * n)
    dist[0] = 0

    heap = [(0, 0)]  # (cost, state), state = vertex + parity * n

    while heap:
        d, state = heapq.heappop(heap)
        if d != dist[state]:
            continue

        v = state % n
        parity = state // n

        if v == n - 1:
            print(d)
            return

        reversed_state = v + (1 - parity) * n
        nd = d + x
        if nd < dist[reversed_state]:
            dist[reversed_state] = nd
            heapq.heappush(heap, (nd, reversed_state))

        neighbors = outgoing[v] if parity == 0 else incoming[v]
        base = parity * n
        nd = d + 1
        for to in neighbors:
            next_state = base + to
            if nd < dist[next_state]:
                dist[next_state] = nd
                heapq.heappush(heap, (nd, next_state))


if __name__ == "__main__":
    solve()