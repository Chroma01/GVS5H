import sys
import heapq

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = int(next(it))

    adj = [[] for _ in range(N)]
    radj = [[] for _ in range(N)]

    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        radj[v].append(u)

    del data, it

    INF = 10**30
    dist = [INF] * (2 * N)

    # state = 2 * vertex + parity
    # parity 0: original edge directions
    # parity 1: all edges reversed
    start = 0
    dist[start] = 0
    heap = [(0, start)]

    heappop = heapq.heappop
    heappush = heapq.heappush
    target = N - 1

    while heap:
        d, state = heappop(heap)
        if d != dist[state]:
            continue

        v = state >> 1
        if v == target:
            print(d)
            return

        parity = state & 1

        # Reverse all edges: toggle parity.
        nd = d + X
        nstate = state ^ 1
        if nd < dist[nstate]:
            dist[nstate] = nd
            heappush(heap, (nd, nstate))

        # Move along one currently active edge.
        nd = d + 1
        if parity == 0:
            for to in adj[v]:
                nstate = to << 1
                if nd < dist[nstate]:
                    dist[nstate] = nd
                    heappush(heap, (nd, nstate))
        else:
            # In reversed orientation, outgoing edges from v are original incoming edges to v.
            for to in radj[v]:
                nstate = (to << 1) | 1
                if nd < dist[nstate]:
                    dist[nstate] = nd
                    heappush(heap, (nd, nstate))

    ans = min(dist[target << 1], dist[(target << 1) | 1])
    print(ans)

if __name__ == "__main__":
    solve()