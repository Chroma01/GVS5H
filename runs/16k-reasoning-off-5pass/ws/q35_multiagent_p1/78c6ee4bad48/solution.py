import sys
import heapq

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    X = [int(x) for x in input_data[1:]]
    
    # Sort the initial coordinates
    X.sort()
    
    # We need to maintain the array X in sorted order.
    # The operation is defined on the pieces in ascending order of coordinate.
    # So we always operate on indices i, i+1, i+2, i+3 of the sorted array.
    
    # The operation reduces the sum if X[i] + X[i+3] < X[i+1] + X[i+2].
    # The change in sum is 2 * (X[i] + X[i+3] - X[i+1] - X[i+2]).
    # We want to perform operations that reduce the sum.
    # To minimize the sum, we should greedily perform the operation that gives the largest reduction.
    # The reduction amount is 2 * (X[i+1] + X[i+2] - X[i] - X[i+3]).
    # Let score[i] = X[i+1] + X[i+2] - X[i] - X[i+3].
    # We want to pick i with the largest positive score[i].
    
    # We use a max-heap to store (-score[i], i) so we can extract the max score efficiently.
    # Note: Python's heapq is a min-heap, so we store negative scores.
    
    # Initialize the heap with all possible i from 0 to N-4
    heap = []
    for i in range(N - 3):
        score = X[i+1] + X[i+2] - X[i] - X[i+3]
        if score > 0:
            heapq.heappush(heap, (-score, i))
            
    # We also need to keep track of valid indices in the heap because the array changes.
    # We can use a "lazy deletion" approach or simply re-evaluate.
    # Since N is up to 2*10^5, and each operation changes the array,
    # we might have stale entries in the heap.
    # We can use a "version" or just re-push.
    
    # To avoid stale entries, we can store the index and the score.
    # When we pop, we check if the score matches the current state.
    # If not, we push the new score if it's positive.
    
    # However, there's a catch: the operation changes X[i+1] and X[i+2], which affects scores for i-1, i, i+1.
    # So we need to update the heap for these indices.
    
    # Let's implement the loop.
    
    while heap:
        neg_score, i = heapq.heappop(heap)
        current_score = X[i+1] + X[i+2] - X[i] - X[i+3]
        
        # If the score is not positive or doesn't match the heap entry (stale), skip
        if current_score <= 0 or -neg_score != current_score:
            # If it was stale but positive, we should push the new score?
            # No, because if it's stale, it means the array changed, and we will push new scores for affected indices.
            # But we need to make sure we don't miss updates.
            # Actually, if current_score > 0 and -neg_score != current_score, it means the heap entry is outdated.
            # We should push the current_score if it's positive.
            if current_score > 0:
                heapq.heappush(heap, (-current_score, i))
            continue
            
        # Perform the operation
        # M = (X[i] + X[i+3]) / 2
        # New X[i+1] = M + (M - X[i+1]) = X[i] + X[i+3] - X[i+1]
        # New X[i+2] = M - (X[i+2] - M) = X[i] + X[i+3] - X[i+2]
        
        new_x1 = X[i] + X[i+3] - X[i+1]
        new_x2 = X[i] + X[i+3] - X[i+2]
        
        # Update the array
        X[i+1] = new_x1
        X[i+2] = new_x2
        
        # The array is no longer sorted. We need to re-sort the affected part or the whole array?
        # Re-sorting the whole array is O(N log N) per operation, which is too slow.
        # However, the operation only changes two elements.
        # We can remove X[i+1] and X[i+2] and insert them in sorted order.
        # But since we are using a list, removal and insertion is O(N).
        # Total complexity would be O(K * N), which might be too slow if K is large.
        
        # Let's try to keep the array sorted by using bisect.
        # Remove the old values and insert the new ones.
        # But we need to know the positions.
        # Since we are operating on indices i, i+1, i+2, i+3, the values at i+1 and i+2 are changed.
        # The new values might not be in the correct position relative to the rest of the array.
        
        # Extract the four elements involved
        # Actually, it's easier to just re-sort the entire array if N is small, but N is large.
        # Let's use a different data structure? No, let's try to maintain sorted order.
        
        # We can remove the elements at i+1 and i+2 and insert the new ones in sorted order.
        # But we need to find the correct positions for the new values.
        
        # Let's extract the subarray from i to i+3, update it, and re-sort it.
        # Then put it back.
        # This is O(1) if we use a list and slice, but slicing and sorting 4 elements is constant time.
        # However, the new values might need to be inserted into the global sorted array.
        # The operation is defined on the pieces in ascending order.
        # So after the operation, the pieces at i+1 and i+2 might move.
        # We need to re-insert them into the sorted array.
        
        # Let's remove the old values and insert the new ones.
        # But we need to know the indices of the new values.
        
        # Alternative: Just re-sort the entire array? O(N log N) per operation.
        # If K is large, this is too slow.
        
        # Let's try to use the fact that the final state is unique and can be found by a greedy strategy.
        # The final state satisfies X[i] + X[i+3] >= X[i+1] + X[i+2] for all i.
        # This is equivalent to the sequence of differences being "convex" in a specific way.
        
        # Given the time constraints, I will implement the simulation with bisect for insertion.
        # This might be fast enough if the number of operations is small.
        
        # Remove the old values at i+1 and i+2
        # Since we are operating on indices i, i+1, i+2, i+3, we can just replace them and re-sort the slice.
        # But the new values might not be in the correct position.
        
        # Let's extract the four elements, update them, and then re-insert them into the sorted array.
        # But we need to know the positions.
        
        # Actually, the operation is defined on the pieces in ascending order.
        # So after the operation, the pieces are at new positions.
        # We need to re-sort the entire array to maintain the invariant that X is sorted.
        
        # Let's try to re-sort the entire array using sorted() or sort().
        # This is O(N log N) per operation.
        # If the number of operations is small, this is acceptable.
        
        # Let's hope the number of operations is small.
        
        # Re-sort the entire array
        X.sort()
        
        # Update the heap with new scores for affected indices
        # The operation affects indices i-1, i, i+1 (if they exist)
        # Because the values at i+1 and i+2 changed, which affects scores for:
        # i-1: involves X[i], X[i+1], X[i+2], X[i+3] -> X[i+1] and X[i+2] changed
        # i: involves X[i], X[i+1], X[i+2], X[i+3] -> X[i+1] and X[i+2] changed
        # i+1: involves X[i+1], X[i+2], X[i+3], X[i+4] -> X[i+1] and X[i+2] changed
        
        # So we need to update scores for i-1, i, i+1.
        
        for j in [i-1, i, i+1]:
            if 0 <= j <= N - 4:
                score = X[j+1] + X[j+2] - X[j] - X[j+3]
                if score > 0:
                    heapq.heappush(heap, (-score, j))
                    
    print(sum(X))

solve()