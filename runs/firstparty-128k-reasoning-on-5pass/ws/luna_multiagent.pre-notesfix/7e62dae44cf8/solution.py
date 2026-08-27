import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    H = next(it)
    W = next(it)
    X = next(it)
    P = next(it) - 1
    Q = next(it) - 1

    n = H * W
    strength_grid = [next(it) for _ in range(n)]

    start = P * W + Q
    current = strength_grid[start]

    visited = bytearray(n)
    visited[start] = 1

    heap = []

    def add_neighbor(r, c):
        if 0 <= r < H and 0 <= c < W:
            idx = r * W + c
            if not visited[idx]:
                visited[idx] = 1
                heapq.heappush(heap, (strength_grid[idx], idx))

    add_neighbor(P - 1, Q)
    add_neighbor(P + 1, Q)
    add_neighbor(P, Q - 1)
    add_neighbor(P, Q + 1)

    while heap:
        value, idx = heap[0]

        if value * X >= current:
            break

        heapq.heappop(heap)
        current += value

        r, c = divmod(idx, W)
        add_neighbor(r - 1, c)
        add_neighbor(r + 1, c)
        add_neighbor(r, c - 1)
        add_neighbor(r, c + 1)

    print(current)


if __name__ == "__main__":
    solve()