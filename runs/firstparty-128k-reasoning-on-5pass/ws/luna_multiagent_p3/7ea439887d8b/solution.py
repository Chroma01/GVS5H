import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline

    n, m, x = map(int, input().split())
    outgoing = [[] for _ in range(n)]
    incoming = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        outgoing[u].append(v)
        incoming[v].append(u)

    inf = 10**30
    dist = [[inf, inf] for _ in range(n)]
    dist[0][0] = 0

    pq = [(0, 0, 0)]  # distance, vertex, parity

    while pq:
        d, v, parity = heapq.heappop(pq)
        if d != dist[v][parity]:
            continue

        if v == n - 1:
            print(d)
            return

        # Reverse all edges.
        nd = d + x
        other = parity ^ 1
        if nd < dist[v][other]:
            dist[v][other] = nd
            heapq.heappush(pq, (nd, v, other))

        # Move along an edge in the current orientation.
        neighbors = outgoing[v] if parity == 0 else incoming[v]
        nd = d + 1
        for to in neighbors:
            if nd < dist[to][parity]:
                dist[to][parity] = nd
                heapq.heappush(pq, (nd, to, parity))


if __name__ == "__main__":
    solve()