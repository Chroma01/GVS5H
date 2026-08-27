import sys
import heapq

def solve():
    input = sys.stdin.readline
    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1; Q -= 1
    S = [list(map(int, input().split())) for _ in range(H)]
    
    cur = S[P][Q]
    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True
    
    heap = []
    # Directions: up, down, left, right
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Initialize heap with adjacent cells of starting position
    for dr, dc in dirs:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
            heapq.heappush(heap, (S[nr][nc], nr, nc))
    
    while heap:
        s, r, c = heapq.heappop(heap)
        if visited[r][c]:
            continue
        # Check condition: s < cur / X  <=>  s * X < cur
        if s * X >= cur:
            break
        # Absorb this slime
        cur += s
        visited[r][c] = True
        # Add newly adjacent cells
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
                heapq.heappush(heap, (S[nr][nc], nr, nc))
    
    print(cur)

if __name__ == "__main__":
    solve()