import heapq
import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    H = int(data[0])
    W = int(data[1])
    X = int(data[2])
    P = int(data[3])
    Q = int(data[4])
    
    # Convert to 0-indexed
    start_r = P - 1
    start_c = Q - 1
    
    S = []
    idx = 5
    for i in range(H):
        row = []
        for j in range(W):
            row.append(int(data[idx]))
            idx += 1
        S.append(row)
    
    # dp[r][c] stores the maximum strength achievable when Takahashi is at cell (r,c)
    # Initialize with -1 (unreachable)
    dp = [[-1] * W for _ in range(H)]
    dp[start_r][start_c] = S[start_r][start_c]
    
    # Priority queue: max-heap by strength, so we store (-strength, r, c)
    pq = [(-S[start_r][start_c], start_r, start_c)]
    
    # Visited array to mark cells that have been popped from the priority queue
    visited = [[False] * W for _ in range(H)]
    
    # Global maximum strength
    global_max = S[start_r][start_c]
    
    # 8 directions for adjacency
    directions = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1),  (1, 0),  (1, 1)]
    
    while pq:
        neg_strength, r, c = heapq.heappop(pq)
        strength = -neg_strength
        
        # If already visited, skip
        if visited[r][c]:
            continue
        visited[r][c] = True
        
        # Update global maximum
        if strength > global_max:
            global_max = strength
        
        # Check all 8 neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
                # Condition: S[nr][nc] < strength / X  =>  X * S[nr][nc] < strength
                if X * S[nr][nc] < strength:
                    new_strength = strength + S[nr][nc]
                    if new_strength > dp[nr][nc]:
                        dp[nr][nc] = new_strength
                        heapq.heappush(pq, (-new_strength, nr, nc))
    
    print(global_max)

if __name__ == '__main__':
    main()