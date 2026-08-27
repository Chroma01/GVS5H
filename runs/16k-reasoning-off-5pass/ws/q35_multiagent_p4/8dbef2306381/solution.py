import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = int(next(iterator))
        B = int(next(iterator))
        
        bad_intervals = []
        for _ in range(M):
            L = int(next(iterator))
            R = int(next(iterator))
            bad_intervals.append((L, R))
    except StopIteration:
        return

    # Construct good intervals
    # Good intervals are the gaps between bad intervals, plus start and end
    good_intervals = []
    
    # Start from 1
    current_start = 1
    
    for L, R in bad_intervals:
        # The interval [current_start, L-1] is good
        if current_start <= L - 1:
            good_intervals.append((current_start, L - 1))
        # Move to after the bad interval
        current_start = R + 1
        
    # Add the last good interval
    if current_start <= N:
        good_intervals.append((current_start, N))
        
    # If N is not reachable (e.g., N is bad, but constraints say R_i < N, so N is good)
    # If there are no good intervals containing N, it's impossible
    if not good_intervals:
        print("No")
        return
        
    # Check if N is in the last good interval
    last_good = good_intervals[-1]
    if last_good[1] < N:
        print("No")
        return
        
    # reachable_intervals is a list of disjoint, sorted intervals [start, end]
    # representing the set of reachable squares in the "frontier" of processed good intervals.
    # Initially, we start at square 1.
    # We need to handle the first good interval specially because 1 is reachable without a jump.
    
    # Let's maintain a list of reachable intervals from all previously processed good intervals
    # that are within distance B of the current good interval's start.
    # However, since we process good intervals in order, we can just maintain the reachable
    # intervals from the immediately preceding good intervals that can influence the current one.
    
    # Actually, a simpler approach:
    # Maintain a list of reachable intervals `reachable` which are the reachable squares
    # in the good intervals processed so far.
    # When processing a new good interval [S, E], we compute the new reachable squares
    # in [S, E] by checking against all reachable intervals from previous good intervals
    # that are within distance B of [S, E].
    # Then, within the current good interval, we propagate reachability.
    
    # Let `reachable_intervals` be the list of reachable intervals from all previous good intervals.
    reachable_intervals = []
    
    # We process each good interval
    for idx, (S, E) in enumerate(good_intervals):
        new_reachable_in_current = []
        
        # For each reachable interval from previous good intervals, compute the squares
        # in [S, E] that are reachable by a single jump.
        for r_start, r_end in reachable_intervals:
            # If the reachable interval is too far to the left, skip it
            if r_end < S - B:
                continue
                
            # The squares in [S, E] reachable from [r_start, r_end] by a jump in [A, B]
            # are those x in [S, E] such that there exists y in [r_start, r_end] with A <= x - y <= B.
            # This is equivalent to y in [x - B, x - A].
            # So x is reachable if [x - B, x - A] intersects [r_start, r_end].
            # This intersection is non-empty iff x - B <= r_end and x - A >= r_start.
            # So x <= r_end + B and x >= r_start + A.
            # Thus, the reachable squares in [S, E] from this interval are:
            # [max(S, r_start + A), min(E, r_end + B)]
            
            start = max(S, r_start + A)
            end = min(E, r_end + B)
            
            if start <= end:
                new_reachable_in_current.append((start, end))
                
        # Now, within the current good interval, we can make multiple jumps.
        # The set of reachable squares in [S, E] is the closure of the entry points
        # (squares reachable from previous intervals) under jumps within [S, E].
        # Since the good interval is contiguous, and jumps are in [A, B],
        # the reachable set from an entry interval [a, b] is the union of
        # [a + k*A, b + k*B] for k >= 0, clipped to [S, E].
        # And since these intervals overlap (as shown in the thought process),
        # the union is a single interval [a, min(E, b + k_max * B)] where k_max is the max number of jumps.
        # But this is not quite right because the intervals might not cover all squares.
        # However, a more robust way is to simulate the BFS within the good interval.
        # But since the good interval can be large, we need an efficient way.
        # Actually, the reachable set from an entry interval [a, b] within [S, E] is:
        # [a, b] U [a+A, b+B] U [a+2A, b+2B] U ...
        # And since these intervals overlap if b - a >= A - B (which is always true since A <= B and b >= a),
        # the union is a single interval [a, min(E, b + k_max * B)] where k_max is the max number of jumps.
        # But this is not correct because the intervals might not cover all squares.
        # In fact, the reachable set is [a, min(E, b + k_max * B)] if the intervals overlap.
        # And they do overlap if b - a >= A - B. Since A <= B, A - B <= 0, and b - a >= 0, so yes.
        # So the reachable set from [a, b] is [a, min(E, b + k_max * B)] where k_max is the largest k such that a + k*A <= E.
        # But this is not correct because we can reach squares between b and a+A if b < a+A.
        # But in our case, the entry points are from previous intervals, so they are disjoint from the current good interval? No.
        # The entry points are in the current good interval.
        # So the reachable set in the current good interval is the union of the reachable sets from each entry interval.
        # And we can merge these reachable sets.
        
        # Let's compute the reachable set from each entry interval in new_reachable_in_current.
        # For each entry interval [a, b], the reachable set is [a, min(E, b + k_max * B)] where k_max is the max number of jumps.
        # But this is not correct. Let's use a different approach.
        # Since B is small, we can simulate the BFS within the good interval if the good interval is small.
        # But if it's large, we can use the fact that the reachable set is an interval if the entry points are dense enough.
        # Actually, the reachable set from an entry interval [a, b] is [a, min(E, b + k_max * B)] where k_max is the max number of jumps.
        # But this is not correct. Let's use the following:
        # The reachable set from an entry interval [a, b] is the union of [a + k*A, b + k*B] for k >= 0.
        # And we can compute this union by finding the max k such that a + k*A <= E.
        # Then the reachable set is the union of these intervals.
        # And we can merge these intervals.
        
        # Since the number of entry intervals is small, and the number of jumps is small, we can compute the reachable set
        # from each entry interval by simulating the BFS for a few jumps.
        # But the good interval can be large, so we can't simulate all jumps.
        # However, note that the reachable set from an entry interval [a, b] is the union of [a + k*A, b + k*B] for k >= 0.
        # And we can compute this union by finding the max k such that a + k*A <= E.
        # Then the reachable set is the union of these intervals.
        # And we can merge these intervals.
        
        # Let's compute the reachable set from each entry interval.
        final_reachable_in_current = []
        
        for a, b in new_reachable_in_current:
            # The reachable set from [a, b] is the union of [a + k*A, b + k*B] for k >= 0, clipped to [S, E].
            # We can compute this by iterating k from 0 to k_max.
            # k_max is the largest k such that a + k*A <= E.
            if a > E:
                continue
                
            k_max = (E - a) // A
            # Generate the intervals
            intervals = []
            for k in range(k_max + 1):
                start_k = a + k * A
                end_k = b + k * B
                # Clip to [S, E]
                start_k = max(S, start_k)
                end_k = min(E, end_k)
                if start_k <= end_k:
                    intervals.append((start_k, end_k))
                    
            # Merge intervals
            if not intervals:
                continue
                
            intervals.sort()
            merged = [intervals[0]]
            for i in range(1, len(intervals)):
                if intervals[i][0] <= merged[-1][1] + 1:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], intervals[i][1]))
                else:
                    merged.append(intervals[i])
                    
            final_reachable_in_current.extend(merged)
            
        # Merge all intervals in final_reachable_in_current
        if not final_reachable_in_current:
            print("No")
            return
            
        final_reachable_in_current.sort()
        merged_final = [final_reachable_in_current[0]]
        for i in range(1, len(final_reachable_in_current)):
            if final_reachable_in_current[i][0] <= merged_final[-1][1] + 1:
                merged_final[-1] = (merged_final[-1][0], max(merged_final[-1][1], final_reachable_in_current[i][1]))
            else:
                merged_final.append(final_reachable_in_current[i])
                
        # Update reachable_intervals to be the reachable intervals in the current good interval
        # for the next iteration.
        reachable_intervals = merged_final
        
    # After processing all good intervals, check if N is reachable.
    # N is in the last good interval.
    # Check if N is in any of the reachable intervals in the last good interval.
    for start, end in reachable_intervals:
        if start <= N <= end:
            print("Yes")
            return
            
    print("No")

solve()