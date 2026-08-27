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
    strengths = [next(it) for _ in range(n)]

    start = P * W + Q
    current = strengths[start]

    visited = bytearray(n)
    visited[start] = 1

    heap = []

    def add_cell(r, c):
        if 0 <= r < H and 0 <= c < W:
            idx = r * W + c
            if not visited[idx]:
                visited[idx] = 1
                heapq.heappush(heap, (strengths[idx], idx))

    add_cell(P - 1, Q)
    add_cell(P + 1, Q)
    add_cell(P, Q - 1)
    add_cell(P, Q + 1)

    while heap:
        value, idx = heap[0]
        if value * X >= current:
            break

        heapq.heappop(heap)
        current += value

        r, c = divmod(idx, W)
        add_cell(r - 1, c)
        add_cell(r + 1, c)
        add_cell(r, c - 1)
        add_cell(r, c + 1)

    print(current)


if __name__ == "__main__":
    solve()