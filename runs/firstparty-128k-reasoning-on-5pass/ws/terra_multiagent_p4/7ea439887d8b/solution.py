import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline
    n, m, x = map(int, input().split())

    out_edges = [[] for _ in range(n)]
    in_edges = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        out_edges[u].append(v)
        in_edges[v].append(u)

    inf = 10**30
    dist = [inf] * (2 * n)
    dist[0] = 0
    pq = [(0, 0)]  # (cost, state), state = 2 * vertex + parity

    while pq:
        d, state = heapq.heappop(pq)
        if d != dist[state]:
            continue

        v = state >> 1
        parity = state & 1

        if v == n - 1:
            print(d)
            return

        reversed_state = state ^ 1
        nd = d + x
        if nd < dist[reversed_state]:
            dist[reversed_state] = nd
            heapq.heappush(pq, (nd, reversed_state))

        if parity == 0:
            neighbors = out_edges[v]
        else:
            neighbors = in_edges[v]

        nd = d + 1
        for to in neighbors:
            next_state = (to << 1) | parity
            if nd < dist[next_state]:
                dist[next_state] = nd
                heapq.heappush(pq, (nd, next_state))


if __name__ == "__main__":
    solve()