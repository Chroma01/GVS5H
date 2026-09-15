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

    out_adj = [[] for _ in range(N + 1)]
    in_adj = [[] for _ in range(N + 1)]

    for _ in range(M):
        u = next(it)
        v = next(it)
        out_adj[u].append(v)
        in_adj[v].append(u)

    INF = 10**30
    dist0 = [INF] * (N + 1)
    dist1 = [INF] * (N + 1)

    dist0[1] = 0
    heap = [(0, 1, 0)]
    heappop = heapq.heappop
    heappush = heapq.heappush

    while heap:
        d, v, layer = heappop(heap)

        if layer == 0:
            if d != dist0[v]:
                continue

            nd = d + 1
            for to in out_adj[v]:
                if nd < dist0[to]:
                    dist0[to] = nd
                    heappush(heap, (nd, to, 0))

            nd = d + X
            if nd < dist1[v]:
                dist1[v] = nd
                heappush(heap, (nd, v, 1))

        else:
            if d != dist1[v]:
                continue

            nd = d + 1
            for to in in_adj[v]:
                if nd < dist1[to]:
                    dist1[to] = nd
                    heappush(heap, (nd, to, 1))

            nd = d + X
            if nd < dist0[v]:
                dist0[v] = nd
                heappush(heap, (nd, v, 0))

    ans = min(dist0[N], dist1[N])
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()