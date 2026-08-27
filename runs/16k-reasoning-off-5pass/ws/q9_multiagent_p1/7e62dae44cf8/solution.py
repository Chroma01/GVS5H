import sys
import heapq

def solve():
    # Read all input from stdin
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
        
        S = []
        for _ in range(H):
            row = []
            for _ in range(W):
                row.append(int(next(iterator)))
            S.append(row)
            
    except StopIteration:
        return

    # Directions for 8-connectivity (King's moves)
    # Up, Down, Left, Right, Up-Left, Up-Right, Down-Left, Down-Right
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    # Priority queue to store available slimes: (strength, r, c)
    pq = []
    
    # Set to keep track of absorbed slimes.
    # Initially empty. The starting cell (P, Q) is occupied by Takahashi, not a slime.
    # We only mark cells as absorbed when Takahashi moves into them and the slime disappears.
    absorbed = set()
    
    # Add all 8 neighbors of the starting position to the priority queue
    # Check bounds
    for dr, dc in directions:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W:
            heapq.heappush(pq, (S[nr][nc], nr, nc))
            
    current_strength = S[P][Q]
    
    # We continue as long as there are valid moves
    # A move is valid if there exists a neighbor in pq with strength < current_strength / X
    
    while pq:
        # Check the smallest strength in the heap
        min_s, r, c = pq[0]
        
        # Condition: strictly less than 1/X times current strength
        # min_s < current_strength / X  <=>  min_s * X < current_strength
        if min_s * X < current_strength:
            # Absorb the slime
            heapq.heappop(pq)
            current_strength += min_s
            
            # Mark the absorbed cell as visited/absorbed
            absorbed.add((r, c))
            
            # The gap is filled by Takahashi, so the cell (r,c) is now empty.
            # The neighbors of (r,c) become newly adjacent.
            # We need to add the neighbors of (r,c) to the priority queue if they are not absorbed.
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    if (nr, nc) not in absorbed:
                        heapq.heappush(pq, (S[nr][nc], nr, nc))
        else:
            # The smallest available slime is too strong. Since the heap is sorted,
            # no other slime in the heap can be absorbed either.
            # We can stop.
            break
            
    print(current_strength)

if __name__ == '__main__':
    solve()