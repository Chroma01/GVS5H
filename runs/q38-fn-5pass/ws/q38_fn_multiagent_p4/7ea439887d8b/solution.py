import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, X = data[0], data[1], data[2]

    g = [[] for _ in range(N + 1)]
    rg = [[] for _ in range(N + 1)]

    idx = 3
    for _ in range(M):
        u = data[idx]
        v = data[idx + 1]
        idx += 2
        g[u].append(v)
        rg[v].append(u)

    del data

    INF = 10**30

    # State index: (vertex << 1) | parity
    # parity 0: original orientation
    # parity 1: reversed orientation
    dist = [INF] * (2 * (N + 1))

    start = 1 << 1
    dist[start] = 0

    heap = [(0, start)]
    heappush = heapq.heappush
    heappop = heapq.heappop

    while heap:
        d, s = heappop(heap)

        if d != dist[s]:
            continue

        v = s >> 1

        if v == N:
            print(d)
            return

        if s & 1:
            # Reversed orientation: use original incoming edges.
            nd = d + 1
            for to in rg[v]:
                ns = (to << 1) | 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    heappush(heap, (nd, ns))

            # Reverse all edges.
            nd = d + X
            ns = s ^ 1
            if nd < dist[ns]:
                dist[ns] = nd
                heappush(heap, (nd, ns))

        else:
            # Original orientation: use original outgoing edges.
            nd = d + 1
            for to in g[v]:
                ns = to << 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    heappush(heap, (nd, ns))

            # Reverse all edges.
            nd = d + X
            ns = s ^ 1
            if nd < dist[ns]:
                dist[ns] = nd
                heappush(heap, (nd, ns))

    ans = min(dist[N << 1], dist[(N << 1) | 1])
    print(ans)


if __name__ == "__main__":
    solve()