import sys
import heapq

# Set recursion limit just in case, though we use an iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
        X = int(next(iterator))
        P = int(next(iterator))
        Q = int(next(iterator))
        
        # Adjust P and Q to 0-based indexing
        P -= 1
        Q -= 1
        
        grid = []
        for _ in range(H):
            row = []
            for _ in range(W):
                row.append(int(next(iterator)))
            grid.append(row)
            
    except StopIteration:
        return

    # Max-heap to store (strength, r, c)
    # Python's heapq is a min-heap, so we store negative strength to simulate max-heap
    pq = []
    
    # dist[r][c] stores the maximum strength Takahashi has achieved upon reaching cell (r, c)
    # Initialize with -1 (since strengths are positive)
    dist = [[-1] * W for _ in range(H)]
    
    # Initial state: Takahashi starts at (P, Q) with strength S[P][Q]
    start_strength = grid[P][Q]
    dist[P][Q] = start_strength
    heapq.heappush(pq, (-start_strength, P, Q))
    
    # Directions for neighbors: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while pq:
        neg_s, r, c = heapq.heappop(pq)
        s = -neg_s
        
        # If we found a better path to (r, c) already, skip
        if s < dist[r][c]:
            continue
        
        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < H and 0 <= nc < W:
                neighbor_strength = grid[nr][nc]
                
                # Check condition: neighbor_strength < s / X
                # Equivalent to: neighbor_strength * X < s (using integer arithmetic to avoid precision issues)
                if neighbor_strength * X < s:
                    new_strength = s + neighbor_strength
                    
                    # If this path gives a higher strength at (nr, nc), update and push to heap
                    if new_strength > dist[nr][nc]:
                        dist[nr][nc] = new_strength
                        heapq.heappush(pq, (-new_strength, nr, nc))
    
    # The answer is the maximum strength reached at any cell
    ans = 0
    for r in range(H):
        for c in range(W):
            if dist[r][c] > ans:
                ans = dist[r][c]
                
    print(ans)

if __name__ == '__main__':
    solve()