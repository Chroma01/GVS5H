import sys
import heapq


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, X = data[0], data[1], data[2]

    adj = [[] for _ in range(N)]
    radj = [[] for _ in range(N)]

    idx = 3
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        adj[u].append(v)
        radj[v].append(u)

    del data

    INF = 10**30
    dist0 = [INF] * N  # original edge directions
    dist1 = [INF] * N  # reversed edge directions
    dist0[0] = 0

    target = N - 1
    heap = [(0, 0)]  # (distance, state), state = 2 * vertex + parity

    heappush = heapq.heappush
    heappop = heapq.heappop

    while heap:
        d, state = heappop(heap)
        v = state >> 1

        if state & 1:
            if d != dist1[v]:
                continue

            if v == target:
                print(d)
                return

            nd = d + 1
            for to in radj[v]:
                if nd < dist1[to]:
                    dist1[to] = nd
                    heappush(heap, (nd, (to << 1) | 1))

            nd = d + X
            if nd < dist0[v]:
                dist0[v] = nd
                heappush(heap, (nd, v << 1))

        else:
            if d != dist0[v]:
                continue

            if v == target:
                print(d)
                return

            nd = d + 1
            for to in adj[v]:
                if nd < dist0[to]:
                    dist0[to] = nd
                    heappush(heap, (nd, to << 1))

            nd = d + X
            if nd < dist1[v]:
                dist1[v] = nd
                heappush(heap, (nd, (v << 1) | 1))

    ans = dist0[target] if dist0[target] < dist1[target] else dist1[target]
    print(ans)


if __name__ == "__main__":
    solve()