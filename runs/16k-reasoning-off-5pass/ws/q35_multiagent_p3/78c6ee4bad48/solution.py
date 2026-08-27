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

    # The problem asks to minimize the sum of coordinates.
    # Operation: Choose i (1 <= i <= N-3). Let the 4 pieces in sorted order be x_i, x_{i+1}, x_{i+2}, x_{i+3}.
    # Midpoint M = (x_i + x_{i+3}) / 2.
    # New positions: x'_{i+1} = M + (M - x_{i+1}) = x_i + x_{i+3} - x_{i+1}
    #                x'_{i+2} = M - (x_{i+2} - M) = x_i + x_{i+3} - x_{i+2}
    # Note: The problem states "i-th and (i+3)-rd pieces in ascending order of coordinate".
    # This implies we always operate on 4 consecutive pieces in the current sorted configuration.
    # The pieces are identified by their rank. So we operate on indices i, i+1, i+2, i+3 of the sorted array.
    
    # The change in sum for the 4 pieces is:
    # New sum of 4 = x_i + (x_i + x_{i+3} - x_{i+1}) + (x_i + x_{i+3} - x_{i+2}) + x_{i+3}
    #              = 3*x_i + 3*x_{i+3} - x_{i+1} - x_{i+2}
    # Old sum of 4 = x_i + x_{i+1} + x_{i+2} + x_{i+3}
    # Delta = New - Old = 2*x_i + 2*x_{i+3} - 2*x_{i+1} - 2*x_{i+2}
    #       = 2 * (x_i + x_{i+3} - x_{i+1} - x_{i+2})
    # The operation reduces the total sum if Delta < 0, i.e., x_i + x_{i+3} < x_{i+1} + x_{i+2}.
    
    # We can use a greedy approach: repeatedly apply operations that reduce the sum.
    # Since N is up to 2*10^5, we need an efficient way to find such operations.
    # A priority queue can store the "potential reduction" for each window.
    # However, applying an operation changes the values, which affects adjacent windows.
    # We can use a lazy deletion approach with a priority queue.
    
    # Store potential reductions. We want to maximize reduction, so store negative of Delta.
    # Delta = 2 * (x_i + x_{i+3} - x_{i+1} - x_{i+2})
    # Reduction = -Delta = 2 * (x_{i+1} + x_{i+2} - x_i - x_{i+3})
    # We only care if Reduction > 0.
    
    # Priority queue stores (-reduction, i) so that we pick the largest reduction.
    pq = []
    
    # Initialize the priority queue with all possible windows
    for i in range(N - 3):
        # Window indices: i, i+1, i+2, i+3
        # Values: X[i], X[i+1], X[i+2], X[i+3]
        reduction = 2 * (X[i+1] + X[i+2] - X[i] - X[i+3])
        if reduction > 0:
            heapq.heappush(pq, (-reduction, i))
            
    # To handle lazy deletion, we can store the current state of the array and check validity.
    # However, since the array changes, we need to be careful.
    # A simpler approach for this specific problem is to note that the operations are local.
    # We can use a stack or a simple loop if the number of operations is small, but it might be large.
    # Given the constraints and problem type, a greedy simulation with PQ is likely intended.
    
    # We need to track the current values of X.
    # When we apply an operation at index i, we update X[i+1] and X[i+2].
    # This affects windows starting at i-1, i, i+1.
    # We can re-evaluate these windows and push them back to the PQ.
    
    # To avoid infinite loops and ensure termination, note that each operation strictly decreases the sum.
    # The sum is bounded below (by the sum of sorted X, or similar).
    
    # However, with N=2*10^5, the number of operations could be large.
    # There is a known result that the minimum sum is achieved when the sequence is "convex".
    # But let's stick to the simulation.
    
    # To make it efficient, we can use a linked list or just an array and update.
    # Since we only update two elements, we can just update the array.
    
    # We also need to handle the fact that the array remains sorted?
    # The problem states "it can be proved that all pieces always occupy distinct coordinates".
    # It does NOT say they remain sorted in the same order.
    # But the operation is defined on the "i-th and (i+3)-rd pieces in ascending order of coordinate".
    # This means we always pick the 1st, 2nd, 3rd, 4th smallest pieces.
    # So the array X is always kept sorted.
    # When we update X[i+1] and X[i+2], we must re-sort the affected part?
    # No, the operation reflects the inner two pieces.
    # The new positions are x'_{i+1} = x_i + x_{i+3} - x_{i+1}
    #                x'_{i+2} = x_i + x_{i+3} - x_{i+2}
    # Since x_i < x_{i+1} < x_{i+2} < x_{i+3}, we have:
    # x'_{i+2} < x'_{i+1} because x_{i+1} < x_{i+2} implies -x_{i+1} > -x_{i+2}.
    # So the new positions are swapped relative to each other?
    # Let's check: x'_{i+1} - x'_{i+2} = (x_i + x_{i+3} - x_{i+1}) - (x_i + x_{i+3} - x_{i+2}) = x_{i+2} - x_{i+1} > 0.
    # So x'_{i+1} > x'_{i+2}.
    # This means the new positions are not in sorted order!
    # The problem says "move each of the (i+1)-th and (i+2)-th pieces ... to positions symmetric to M".
    # The pieces are identified by their rank. So after the move, the piece that was at x_{i+1} is now at x'_{i+1},
    # and the piece that was at x_{i+2} is now at x'_{i+2}.
    # Since x'_{i+2} < x'_{i+1}, the new sorted order will have the piece that was at x_{i+2} before the piece that was at x_{i+1}.
    # This means the pieces swap their relative order in the sorted list.
    # So we need to update the array and re-sort the affected elements?
    # Actually, since only two elements change, and they swap order, we can just swap them in the array.
    # But we must ensure the entire array is sorted.
    # Since x_i < x'_{i+2} < x'_{i+1} < x_{i+3} is not necessarily true.
    # Let's check:
    # x'_{i+2} = x_i + x_{i+3} - x_{i+2}. Since x_{i+2} < x_{i+3}, x'_{i+2} > x_i.
    # x'_{i+1} = x_i + x_{i+3} - x_{i+1}. Since x_{i+1} > x_i, x'_{i+1} < x_{i+3}.
    # So x_i < x'_{i+2} < x'_{i+1} < x_{i+3} is true if x'_{i+2} < x'_{i+1}, which is true.
    # So the new values are still between x_i and x_{i+3}.
    # And since x'_{i+2} < x'_{i+1}, the sorted order of the 4 elements becomes:
    # x_i, x'_{i+2}, x'_{i+1}, x_{i+3}.
    # So in the array, we replace X[i+1] and X[i+2] with X[i+2] and X[i+1] (swapped) but with new values?
    # No, the values change.
    # The new values are v1 = x_i + x_{i+3} - x_{i+1} and v2 = x_i + x_{i+3} - x_{i+2}.
    # And v2 < v1.
    # So the new sorted sequence for these 4 positions is x_i, v2, v1, x_{i+3}.
    # So we set X[i+1] = v2 and X[i+2] = v1.
    # This maintains the sorted order of the entire array!
    # Because X[i] < v2 and v1 < X[i+3] and v2 < v1.
    # And we need to check X[i-1] < X[i] and X[i+3] < X[i+4].
    # Since X[i] and X[i+3] are unchanged, and the array was sorted, the new array is still sorted.
    
    # So the update is:
    # v1 = X[i] + X[i+3] - X[i+1]
    # v2 = X[i] + X[i+3] - X[i+2]
    # X[i+1] = v2
    # X[i+2] = v1
    
    # This is efficient. We can just update the array.
    
    # We need to re-evaluate windows i-1, i, i+1 after the update.
    # We can push them to the PQ.
    
    # To handle lazy deletion, we can store the current values of X in the PQ?
    # No, we can just check if the reduction is still positive and if the values match the current state.
    # But since we update the array, the old entries in PQ are stale.
    # We can use a version counter or just re-push and ignore stale entries.
    # A simple way is to store the current sum of the window in the PQ and check against current X.
    # But the sum changes.
    # Instead, we can just re-evaluate the windows and push them.
    # If the PQ contains an entry for window i that is no longer valid (because we updated it),
    # we can check if the current reduction matches the one in PQ.
    # But it's easier to just push all affected windows and let the PQ handle duplicates.
    # We need to ensure we don't process the same window multiple times with stale data.
    # We can store the current "reduction" for each window in an array and check.
    
    # Let's use a simpler approach:
    # Since each operation reduces the sum, and the sum is bounded, it terminates.
    # We can use a set of active windows.
    
    # However, for N=2*10^5, the number of operations might be large.
    # There is a known result that the minimum sum is achieved when the sequence is "convex".
    # But let's try the simulation.
    
    # To avoid TLE, we can use a priority queue and lazy deletion.
    # We store (-reduction, i) in PQ.
    # We also store the current reduction for each window in an array `current_reduction`.
    # When we pop from PQ, we check if the reduction matches `current_reduction[i]`.
    # If not, we skip.
    
    current_reduction = [0] * (N - 2)
    
    for i in range(N - 3):
        r = 2 * (X[i+1] + X[i+2] - X[i] - X[i+3])
        current_reduction[i] = r
        if r > 0:
            heapq.heappush(pq, (-r, i))
            
    while pq:
        neg_r, i = heapq.heappop(pq)
        r = -neg_r
        
        # Check if this entry is stale
        if r != current_reduction[i]:
            continue
            
        # Apply operation
        # New values
        v1 = X[i] + X[i+3] - X[i+1]
        v2 = X[i] + X[i+3] - X[i+2]
        
        # Update array
        X[i+1] = v2
        X[i+2] = v1
        
        # Update current_reduction for affected windows: i-1, i, i+1
        for j in [i-1, i, i+1]:
            if 0 <= j <= N - 4:
                new_r = 2 * (X[j+1] + X[j+2] - X[j] - X[j+3])
                if new_r != current_reduction[j]:
                    current_reduction[j] = new_r
                    if new_r > 0:
                        heapq.heappush(pq, (-new_r, j))
                        
    print(sum(X))

solve()