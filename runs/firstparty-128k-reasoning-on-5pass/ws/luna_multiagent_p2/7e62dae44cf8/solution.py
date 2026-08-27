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

    grid = [[next(it) for _ in range(W)] for _ in range(H)]

    current = grid[P][Q]
    seen = [[False] * W for _ in range(H)]
    seen[P][Q] = True

    heap = []

    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ni, nj = P + di, Q + dj
        if 0 <= ni < H and 0 <= nj < W and not seen[ni][nj]:
            seen[ni][nj] = True
            heapq.heappush(heap, (grid[ni][nj], ni, nj))

    while heap and heap[0][0] * X < current:
        value, i, j = heapq.heappop(heap)
        current += value

        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W and not seen[ni][nj]:
                seen[ni][nj] = True
                heapq.heappush(heap, (grid[ni][nj], ni, nj))

    print(current)


if __name__ == "__main__":
    solve()