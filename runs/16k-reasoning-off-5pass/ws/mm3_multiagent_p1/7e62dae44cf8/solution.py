import heapq

def solve():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0
    H = int(input_data[idx]); idx += 1
    W = int(input_data[idx]); idx += 1
    X = int(input_data[idx]); idx += 1
    P = int(input_data[idx]) - 1; idx += 1
    Q = int(input_data[idx]) - 1; idx += 1
    
    S = []
    for i in range(H):
        row = []
        for j in range(W):
            row.append(int(input_data[idx])); idx += 1
        S.append(row)
    
    cur = S[P][Q]
    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True
    
    # Max-heap using negative values
    heap = []
    
    # Directions: up, down, left, right
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Add initial neighbors
    for dr, dc in dirs:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
            strength = S[nr][nc]
            if strength * X < cur:
                heapq.heappush(heap, (-strength, nr, nc))
    
    while heap:
        neg_strength, r, c = heapq.heappop(heap)
        strength = -neg_strength
        
        # Check if still valid (strength * X < cur)
        if strength * X >= cur:
            # This cell cannot be absorbed now, skip
            continue
        
        # Absorb this cell
        cur += strength
        visited[r][c] = True
        
        # Add its neighbors
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
                n_strength = S[nr][nc]
                if n_strength * X < cur:
                    heapq.heappush(heap, (-n_strength, nr, nc))
    
    print(cur)

if __name__ == "__main__":
    solve()