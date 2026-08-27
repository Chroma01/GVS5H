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

    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for dr, dc in directions:
        nr = P + dr
        nc = Q + dc
        if 0 <= nr < H and 0 <= nc < W:
            visited[nr][nc] = True
            heapq.heappush(heap, (grid[nr][nc], nr, nc))

    while heap:
        value, r, c = heap[0]

        if value * X >= strength:
            break

        heapq.heappop(heap)
        strength += value

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
                visited[nr][nc] = True
                heapq.heappush(heap, (grid[nr][nc], nr, nc))

    print(strength)


if __name__ == "__main__":
    main()