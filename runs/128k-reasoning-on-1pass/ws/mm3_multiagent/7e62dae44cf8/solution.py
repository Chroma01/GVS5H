import sys
import heapq

def solve():
    input = sys.stdin.readline
    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1
    Q -= 1
    grid = [list(map(int, input().split())) for _ in range(H)]

    total = grid[P][Q]
    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True

    heap = []
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ni, nj = P + di, Q + dj
        if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
            heapq.heappush(heap, (grid[ni][nj], ni, nj))

    while heap:
        s, i, j = heapq.heappop(heap)
        if visited[i][j]:
            continue
        # Can absorb only if s * X < total.
        # Use integer arithmetic to avoid overflow: s <= (total-1)//X.
        if s > (total - 1) // X:
            break
        total += s
        visited[i][j] = True
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
                heapq.heappush(heap, (grid[ni][nj], ni, nj))

    print(total)

if __name__ == "__main__":
    solve()