import sys
import heapq

def solve():
    # Read all input at once for efficiency
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    
    H = int(next(it))
    W = int(next(it))
    X = int(next(it))
    P = int(next(it)) - 1  # Convert to 0-indexed
    Q = int(next(it)) - 1  # Convert to 0-indexed
    
    S = []
    for _ in range(H):
        row = [int(next(it)) for _ in range(W)]
        S.append(row)
        
    # Current strength of Takahashi
    current_strength = S[P][Q]
    
    # State array: 0 = unvisited, 1 = in priority queue, 2 = absorbed
    state = [[0] * W for _ in range(H)]
    state[P][Q] = 2
    
    # Min-heap priority queue storing (strength, r, c)
    pq = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Add initial neighbors to PQ
    for dr, dc in dirs:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W and state[nr][nc] == 0:
            state[nr][nc] = 1
            heapq.heappush(pq, (S[nr][nc], nr, nc))
            
    while pq:
        s, r, c = heapq.heappop(pq)
        
        # If already absorbed, skip
        if state[r][c] == 2:
            continue
            
        # Check absorption condition: S_target < current_strength / X
        # Equivalent to S_target * X < current_strength to avoid float precision issues
        if S[r][c] * X < current_strength:
            # Absorb the slime
            state[r][c] = 2
            current_strength += S[r][c]
            
            # Add newly adjacent slimes to PQ
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and state[nr][nc] == 0:
                    state[nr][nc] = 1
                    heapq.heappush(pq, (S[nr][nc], nr, nc))
        else:
            # Since PQ is a min-heap, if the weakest available slime cannot be absorbed,
            # no other slime can be absorbed either. We can safely terminate.
            break
            
    print(current_strength)

if __name__ == '__main__':
    solve()