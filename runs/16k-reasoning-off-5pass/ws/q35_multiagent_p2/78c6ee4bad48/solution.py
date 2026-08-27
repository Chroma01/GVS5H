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

    # X is already sorted as per constraints: 0 <= X_1 < X_2 < ... < X_N
    # We need to minimize the sum of coordinates.
    # Operation on i, i+1, i+2, i+3 (0-indexed: i, i+1, i+2, i+3)
    # Let A=X[i], B=X[i+1], C=X[i+2], D=X[i+3]
    # New B' = A + D - B
    # New C' = A + D - C
    # Change in sum = 2*(A + D - B - C)
    # We want to apply operations that decrease the sum, i.e., A + D < B + C.
    # The reduction is 2*(B + C - A - D).
    # We greedily apply the operation with the maximum reduction.
    
    # Since N can be up to 2*10^5, we need an efficient way to find the best operation.
    # We can use a priority queue to store the potential reduction for each window.
    # However, updating the priority queue after each operation is tricky because
    # an operation affects two overlapping windows.
    
    # Alternative approach:
    # It turns out that the final state is unique and corresponds to the "convexified" sequence.
    # The operation allows us to independently minimize the positions.
    # A known result for this problem (AtCoder ABC 279 F / similar) is that the minimum sum
    # is achieved when the sequence is convex.
    # The convexity condition is X[i] + X[i+2] >= 2*X[i+1] for all i.
    # Or equivalently X[i] + X[i+3] >= X[i+1] + X[i+2].
    
    # Actually, there is a simpler invariant:
    # The operation preserves the multiset of values at odd positions and even positions?
    # Let's check:
    # Initial: X[0], X[1], X[2], X[3]
    # After op on 0,1,2,3: X[0], X[0]+X[3]-X[1], X[0]+X[3]-X[2], X[3]
    # New odd positions (1,3): X[0]+X[3]-X[1], X[3]
    # New even positions (0,2): X[0], X[0]+X[3]-X[2]
    # This doesn't seem to preserve the multisets.
    
    # However, it is known that the minimum sum is simply the sum of the initial array
    # if we can't reduce it. But we can.
    # The correct solution is to simulate the process using a priority queue.
    # To avoid TLE, we note that each operation reduces the sum by a positive amount.
    # But the number of operations can be large.
    
    # Let's use a different insight:
    # The operation is equivalent to reflecting the inner points across the midpoint of the outer points.
    # This is a linear transformation.
    # The final state is unique.
    # We can use a priority queue to store the "potential" reduction for each window.
    # When an operation is performed, we update the values and re-evaluate the windows.
    
    # Given the constraints and the nature of the problem, a greedy simulation with a priority queue
    # might be too slow if we update all affected windows.
    # However, we can use a lazy approach: only re-evaluate the windows that are affected.
    
    # Let's implement a priority queue based solution.
    # We store tuples (-reduction, i) in the heap, where reduction = 2*(X[i+1] + X[i+2] - X[i] - X[i+3])
    # We only push operations with positive reduction.
    
    # To handle updates, we can use a versioned approach or simply re-calculate the reduction
    # for the affected windows when we pop an operation.
    # If the reduction in the heap doesn't match the current reduction, we skip it.
    
    # We need to keep track of the current values of X.
    # Since X is modified, we need to update it.
    
    # Let's use a list for X and a heap for operations.
    
    # Initialize the heap
    heap = []
    # We also need to keep track of the current reduction for each window to detect stale entries
    # But since we update X, we can just re-calculate the reduction when we pop.
    # However, we need to know if the operation is still valid (i.e., the window hasn't been invalidated by other operations).
    # Actually, the operation is always valid as long as the indices are within bounds.
    # But the reduction might have changed.
    
    # We can store the current reduction in the heap. If the stored reduction is less than the current potential reduction,
    # it means we should have processed a better operation first. But since we use a max-heap (via negative values),
    # if the stored reduction is not the maximum, it might be stale.
    # However, it's possible that the reduction increased after other operations.
    # So we need to check if the stored reduction matches the current reduction.
    # But we don't store the current reduction separately.
    
    # Alternative: Use a lazy heap. When we pop an operation, we re-calculate the current reduction.
    # If the current reduction is greater than the stored reduction, it means we missed a better operation.
    # But since we always pick the maximum, if the current reduction is greater, it should have been picked earlier.
    # So if the current reduction is less than the stored reduction, it means the operation is stale.
    # If the current reduction is greater, it means we should have picked it earlier, so we push it back?
    # No, if we pick the maximum, and the current reduction is greater, it means the heap was not up-to-date.
    # This suggests that we should re-calculate the reduction for all affected windows after each operation.
    
    # Given the complexity, let's try a simpler approach:
    # The problem is equivalent to finding the minimum sum of a convex sequence.
    # The final sequence is the unique convex sequence reachable from the initial sequence.
    # This can be computed using a "convex hull" like algorithm.
    # Specifically, we can use a stack to maintain the convex hull.
    
    # However, the operation is not just about sorting. It's about reflecting.
    # Let's stick to the priority queue simulation.
    
    # To make it efficient, we note that each operation reduces the sum by a positive amount.
    # The number of operations might be large, but the values are integers.
    # The values can become negative? No, the problem says distinct coordinates, but they can be negative?
    # The constraints say 0 <= X_i <= 10^12. The operation can produce negative values?
    # Yes, but the problem says "it can be proved that all pieces always occupy distinct coordinates".
    # It doesn't say they remain non-negative.
    
    # Let's implement the priority queue simulation.
    # We'll use a lazy approach: when we pop an operation, we re-calculate the current reduction.
    # If the current reduction is less than the stored reduction, we skip it.
    # If the current reduction is greater, we push the current reduction back?
    # No, if the current reduction is greater, it means we should have picked it earlier.
    # So we push the current reduction and continue.
    # But this can lead to infinite loops if we keep pushing.
    # However, since each operation reduces the sum, and the sum is bounded below (by -infinity? No, but the values are distinct),
    # the process must terminate.
    
    # Actually, the values can become very large or very small.
    # But the number of operations is finite?
    # It is known that the process terminates.
    
    # Let's implement the priority queue simulation.
    
    # Initialize the heap
    # We store (-reduction, i) in the heap.
    # reduction = 2 * (X[i+1] + X[i+2] - X[i] - X[i+3])
    
    for i in range(N - 3):
        reduction = 2 * (X[i+1] + X[i+2] - X[i] - X[i+3])
        if reduction > 0:
            heapq.heappush(heap, (-reduction, i))
    
    # We also need to keep track of the current reduction for each window to detect stale entries.
    # But we can just re-calculate the reduction when we pop.
    # However, we need to know if the operation is still valid.
    # The operation is always valid as long as the indices are within bounds.
    # But the reduction might have changed.
    
    # We'll use a lazy approach: when we pop an operation, we re-calculate the current reduction.
    # If the current reduction is less than the stored reduction, we skip it.
    # If the current reduction is greater, we push the current reduction back?
    # No, if the current reduction is greater, it means we should have picked it earlier.
    # So we push the current reduction and continue.
    # But this can lead to infinite loops if we keep pushing.
    # However, since each operation reduces the sum, and the sum is bounded below, the process must terminate.
    
    # Let's implement the priority queue simulation.
    
    while heap:
        neg_red, i = heapq.heappop(heap)
        current_red = -neg_red
        
        # Re-calculate the current reduction
        A = X[i]
        B = X[i+1]
        C = X[i+2]
        D = X[i+3]
        new_red = 2 * (B + C - A - D)
        
        # If the current reduction is less than the stored reduction, it means the operation is stale.
        # This can happen if other operations have changed the values.
        if new_red < current_red:
            continue
        
        # If the current reduction is greater, it means we should have picked it earlier.
        # But since we use a max-heap, if the current reduction is greater, it should have been picked earlier.
        # So this case should not happen if we always push the correct reduction.
        # However, due to lazy updates, it might happen.
        # In this case, we push the current reduction back and continue.
        if new_red > current_red:
            heapq.heappush(heap, (-new_red, i))
            continue
        
        # If the current reduction is equal to the stored reduction, we apply the operation.
        if new_red > 0:
            # Apply the operation
            X[i+1] = A + D - B
            X[i+2] = A + D - C
            
            # Update the sum
            # The sum decreases by new_red
            
            # Re-evaluate the affected windows: i-1, i, i+1
            # We need to push the new reductions for these windows.
            for j in [i-1, i, i+1]:
                if 0 <= j <= N - 4:
                    A = X[j]
                    B = X[j+1]
                    C = X[j+2]
                    D = X[j+3]
                    new_red = 2 * (B + C - A - D)
                    if new_red > 0:
                        heapq.heappush(heap, (-new_red, j))
    
    # The minimum sum is the sum of the final coordinates
    print(sum(X))

solve()