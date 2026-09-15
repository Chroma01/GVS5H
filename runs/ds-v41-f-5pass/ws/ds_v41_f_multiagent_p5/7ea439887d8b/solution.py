import sys
import heapq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    N = next(it)
    M = next(it)
    X = next(it)

    adj = [[] for _ in range(N + 1)]
    radj = [[] for _ in range(N + 1)]

    for _ in range(M):
        u = next(it)
        v = next(it)
        adj[u].append(v)
        radj[v].append(u)

    INF = 10**30
    dist0 = [INF] * (N + 1)
    dist1 = [INF] * (N + 1)

    dist0[1] = 0
    heap = [(0, 1, 0)]  # cost, vertex, parity (0 = original, 1 = reversed)

    while heap:
        d, v, p = heapq.heappop(heap)

        if p == 0:
            if d != dist0[v]:
                continue
            if v == N:
                print(d)
                return

            # Move along an original directed edge.
            nd = d + 1
            for u in adj[v]:
                if nd < dist0[u]:
                    dist0[u] = nd
                    heapq.heappush(heap, (nd, u, 0))

            # Reverse all edges.
            nd = d + X
            if nd < dist1[v]:
                dist1[v] = nd
                heapq.heappush(heap, (nd, v, 1))

        else:
            if d != dist1[v]:
                continue
            if v == N:
                print(d)
                return

            # In the reversed graph, outgoing edges are original incoming edges.
            nd = d + 1
            for u in radj[v]:
                if nd < dist1[u]:
                    dist1[u] = nd
                    heapq.heappush(heap, (nd, u, 1))

            # Reverse all edges again.
            nd = d + X
            if nd < dist0[v]:
                dist0[v] = nd
                heapq.heappush(heap, (nd, v, 0))

    # The statement guarantees reachability, but keep a safe fallback.
    print(min(dist0[N], dist1[N]))


if __name__ == "__main__":
    main()