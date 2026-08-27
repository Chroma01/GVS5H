import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline
    n, m, x = map(int, input().split())

    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        forward[u].append(v)
        backward[v].append(u)

    inf = 10**30
    dist = [inf] * (2 * n)
    dist[0] = 0
    heap = [(0, 0)]

    while heap:
        d, state = heapq.heappop(heap)
        if d != dist[state]:
            continue

        v = state % n
        orientation = state // n

        if v == n - 1:
            print(d)
            return

        opposite = state + n if orientation == 0 else state - n
        nd = d + x
        if nd < dist[opposite]:
            dist[opposite] = nd
            heapq.heappush(heap, (nd, opposite))

        neighbors = forward[v] if orientation == 0 else backward[v]
        base = n if orientation else 0
        nd = d + 1
        for to in neighbors:
            nxt = base + to
            if nd < dist[nxt]:
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))


if __name__ == "__main__":
    solve()