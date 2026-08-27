import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = map(int, data)
    N = next(it)
    M = next(it)
    X = next(it)

    out = [[] for _ in range(N)]
    inn = [[] for _ in range(N)]

    for _ in range(M):
        u = next(it) - 1
        v = next(it) - 1
        out[u].append(v)
        inn[v].append(u)

    del data, it

    INF = 10**30
    dist = [INF] * (2 * N)
    target_v = N - 1
    start = 0  # vertex 0, layer 0
    dist[start] = 0

    heap = [(0, start)]
    heappush = heapq.heappush
    heappop = heapq.heappop

    while heap:
        d, s = heappop(heap)
        if d != dist[s]:
            continue

        v = s >> 1
        if v == target_v:
            print(d)
            return

        # Reverse all edges: toggle layer at the same vertex.
        flip = s ^ 1
        nd = d + X
        if nd < dist[flip]:
            dist[flip] = nd
            heappush(heap, (nd, flip))

        # Move along one directed edge in the current orientation.
        nd = d + 1
        if s & 1:
            adj = inn[v]
            bit = 1
        else:
            adj = out[v]
            bit = 0

        for u in adj:
            ns = (u << 1) | bit
            if nd < dist[ns]:
                dist[ns] = nd
                heappush(heap, (nd, ns))

    # Fallback; reachability is guaranteed by the statement.
    print(min(dist[target_v << 1], dist[(target_v << 1) | 1]))

if __name__ == "__main__":
    main()