import sys
import heapq


def main():
    input = sys.stdin.buffer.readline

    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1
    Q -= 1

    grid = [list(map(int, input().split())) for _ in range(H)]

    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True

    strength = grid[P][Q]
    heap = []

    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ni, nj = P + di, Q + dj
        if 0 <= ni < H and 0 <= nj < W:
            visited[ni][nj] = True
            heapq.heappush(heap, (grid[ni][nj], ni, nj))

    while heap:
        value, i, j = heap[0]

        if value * X >= strength:
            break

        heapq.heappop(heap)
        strength += value

        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
                visited[ni][nj] = True
                heapq.heappush(heap, (grid[ni][nj], ni, nj))

    print(strength)


if __name__ == "__main__":
    main()