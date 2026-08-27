import sys
from heapq import heappush, heappop

def main():
    vals = list(map(int, sys.stdin.buffer.read().split()))
    if not vals:
        return

    N = vals[0]
    M = vals[1]
    X = vals[2]

    out = [[] for _ in range(N)]
    inn = [[] for _ in range(N)]

    idx = 3
    for _ in range(M):
        u = vals[idx] - 1
        v = vals[idx + 1] - 1
        idx += 2
        out[u].append(v)
        inn[v].append(u)

    del vals

    INF = 10**30
    dist = [INF] * (2 * N)
    dist[0] = 0
    heap = [(0, 0)]
    target = N - 1

    while heap:
        d, s = heappop(heap)
        if d != dist[s]:
            continue

        v = s >> 1
        if v == target:
            print(d)
            return

        if (s & 1) == 0:
            nd = d + 1
            for to in out[v]:
                ns = to << 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    heappush(heap, (nd, ns))

            nd = d + X
            ns = s ^ 1
            if nd < dist[ns]:
                dist[ns] = nd
                heappush(heap, (nd, ns))
        else:
            nd = d + 1
            for to in inn[v]:
                ns = (to << 1) | 1
                if nd < dist[ns]:
                    dist[ns] = nd
                    heappush(heap, (nd, ns))

            nd = d + X
            ns = s ^ 1
            if nd < dist[ns]:
                dist[ns] = nd
                heappush(heap, (nd, ns))

    print(min(dist[target << 1], dist[(target << 1) | 1]))

if __name__ == "__main__":
    main()