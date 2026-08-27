import sys
import heapq


def main():
    input = sys.stdin.buffer.readline

    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1
    Q -= 1

    grid = [list(map(int, input().split())) for _ in range(H)]

    visited = bytearray(H * W)
    start = P * W + Q
    visited[start] = 1

    strength = grid[P][Q]
    heap = []

    def add_neighbors(r, c):
        if r > 0:
            nr, nc = r - 1, c
            idx = nr * W + nc
            if not visited[idx]:
                visited[idx] = 1
                heapq.heappush(heap, (grid[nr][nc], nr, nc))
        if r + 1 < H:
            nr, nc = r + 1, c
            idx = nr * W + nc
            if not visited[idx]:
                visited[idx] = 1
                heapq.heappush(heap, (grid[nr][nc], nr, nc))
        if c > 0:
            nr, nc = r, c - 1
            idx = nr * W + nc
            if not visited[idx]:
                visited[idx] = 1
                heapq.heappush(heap, (grid[nr][nc], nr, nc))
        if c + 1 < W:
            nr, nc = r, c + 1
            idx = nr * W + nc
            if not visited[idx]:
                visited[idx] = 1
                heapq.heappush(heap, (grid[nr][nc], nr, nc))

    add_neighbors(P, Q)

    while heap and heap[0][0] * X < strength:
        value, r, c = heapq.heappop(heap)
        strength += value
        add_neighbors(r, c)

    print(strength)


if __name__ == "__main__":
    main()