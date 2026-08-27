import sys
import heapq

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        X = []
        for _ in range(N):
            X.append(int(next(iterator)))
    except StopIteration:
        return

    # X is already sorted as per problem statement (X_1 < X_2 < ... < X_N)
    # We will maintain X as a list of integers.
    
    # Priority Queue stores tuples: (-reduction, i)
    # We use negative reduction because heapq is a min-heap.
    # i is the index of the operation (0-based, corresponding to problem's 1-based i)
    # The operation at index i involves X[i], X[i+1], X[i+2], X[i+3]
    # Reduction = 2 * (X[i] + X[i+3] - X[i+1] - X[i+2])
    # We want to maximize reduction, so we store -reduction.
    
    pq = []
    
    # Precompute all possible moves
    # Valid i ranges from 0 to N-4 (0-based)
    for i in range(N - 3):
        reduction = 2 * (X[i] + X[i+3] - X[i+1] - X[i+2])
        if reduction > 0:
            heapq.heappush(pq, (-reduction, i))
            
    current_sum = sum(X)
    
    while pq:
        neg_red, i = heapq.heappop(pq)
        red = -neg_red
        
        # Recalculate actual reduction based on current X
        # Check if this move is still valid (reduction > 0)
        # Note: The reduction value in the heap might be stale because X[i+1] or X[i+2] 
        # might have been updated by a previous operation.
        
        actual_red = 2 * (X[i] + X[i+3] - X[i+1] - X[i+2])
        
        if actual_red <= 0:
            continue
            
        # Apply the operation
        # The operation reflects X[i+1] and X[i+2] across the midpoint of X[i] and X[i+3]
        # New X[i+1] = X[i] + X[i+3] - X[i+1]
        # New X[i+2] = X[i] + X[i+3] - X[i+2]
        # Note: The problem states we move the pieces. The piece originally at i+1 moves to new pos A.
        # The piece originally at i+2 moves to new pos B.
        # Since B < A, the sorted order becomes X[i], B, A, X[i+3].
        # So in our sorted array X, index i+1 gets B, and index i+2 gets A.
        
        val_i = X[i]
        val_i3 = X[i+3]
        
        new_val_i1 = val_i + val_i3 - X[i+1]
        new_val_i2 = val_i + val_i3 - X[i+2]
        
        X[i+1] = new_val_i2 # Smaller value goes to i+1
        X[i+2] = new_val_i1 # Larger value goes to i+2
        
        current_sum -= actual_red
        
        # The operation affects the validity/reduction of moves involving indices:
        # i-2, i-1, i, i+1, i+2
        # We need to re-evaluate these and push them back if they are valid.
        # We only push if they are within bounds and have positive reduction.
        
        affected_indices = set()
        for delta in [-2, -1, 0, 1, 2]:
            idx = i + delta
            if 0 <= idx <= N - 4:
                affected_indices.add(idx)
        
        for idx in affected_indices:
            # Calculate reduction for this index
            r = 2 * (X[idx] + X[idx+3] - X[idx+1] - X[idx+2])
            if r > 0:
                heapq.heappush(pq, (-r, idx))
                
    print(current_sum)

if __name__ == '__main__':
    solve()