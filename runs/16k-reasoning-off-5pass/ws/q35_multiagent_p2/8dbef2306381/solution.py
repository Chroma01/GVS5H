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

    # If N is small enough, we can simulate directly
    # But N can be up to 10^12, so we need the interval-based approach.
    
    # We maintain a set of reachable positions.
    # To handle large N, we process intervals.
    # The reachable positions will be maintained as a sorted list of disjoint intervals.
    # Initially, we are at square 1.
    
    # reachable_intervals: list of (start, end) tuples, sorted, non-overlapping
    reachable_intervals = [(1, 1)]
    
    # Current position tracker for processing
    # We process bad intervals in order.
    # Let's define the "current end" of processed squares.
    # We start at 1. The next square to consider is 2.
    
    # Helper function to check if a position is bad
    # We'll use the bad_intervals list which is sorted by L.
    
    # We need to process the good intervals between bad intervals.
    # Let's add a virtual bad interval at the end to handle the final stretch to N?
    # No, we just need to check if N is reachable.
    
    # Let's process each bad interval.
    # Before each bad interval [L, R], there is a good interval (prev_bad_end + 1, L - 1).
    # We need to propagate reachability through this good interval.
    
    prev_bad_end = 0
    
    for (L_bad, R_bad) in bad_intervals:
        # Good interval before this bad interval: [prev_bad_end + 1, L_bad - 1]
        start_good = prev_bad_end + 1
        end_good = L_bad - 1
        
        if start_good <= end_good:
            # Propagate reachability through [start_good, end_good]
            # We need to find all positions in [start_good, end_good] that are reachable.
            
            # We can simulate step by step, but if the interval is long, we optimize.
            # Optimization: If at any point, the reachable set contains a contiguous interval of length >= B,
            # then all subsequent positions in the good interval are reachable.
            
            # Let's maintain a list of reachable intervals within the current good interval.
            # We start with the reachable intervals that can reach into this good interval.
            
            # First, filter reachable_intervals to only those that can reach into [start_good, end_good]
            # A reachable interval [u, v] can reach into [start_good, end_good] if:
            # u + B >= start_good and v + A <= end_good (roughly)
            # More precisely, a position x in [u, v] can reach y if x + A <= y <= x + B.
            # So y is reachable if there exists x in [u, v] such that y - B <= x <= y - A.
            
            # We'll compute the new reachable intervals in [start_good, end_good].
            
            new_reachable = []
            
            # We can process the good interval step by step if it's short, or use the optimization.
            # Since B is small (<= 20), the "window" of influence is small.
            # We can simulate for a few steps. If the good interval is very long, we detect stabilization.
            
            # Let's simulate up to a certain limit, say 2*B*B or similar, to detect if we get a contiguous block.
            # Actually, if we have a contiguous reachable interval of length B, the next step produces a contiguous interval of length B.
            # If the good interval is longer than B, and we have such a block, all subsequent positions are reachable.
            
            # Let's define a threshold for "long" interval.
            # If the length of the good interval is greater than, say, 2 * B * max(A, B), we can use the optimization.
            # But a simpler bound: if we have a contiguous reachable interval of length >= B, then all positions in the good interval are reachable.
            # Why? Because from any position in a contiguous block of size B, we can jump to the next B positions.
            # If the block is [x, x+B-1], the next reachable positions are [x+A, x+2B-1].
            # If A <= B, then x+A <= x+B, so the intervals overlap or touch.
            # The union is [x+A, x+2B-1]. The length is B.
            # If we continue, we get [x+2A, x+3B-1], etc.
            # As long as the good interval is long enough, the reachable set becomes a contiguous interval.
            # Specifically, if we have a contiguous reachable interval of length B, then all subsequent positions in the good interval are reachable.
            
            # Let's simulate step by step for the good interval, but keep track of the "frontier".
            # We can use a boolean array for the last B positions to determine reachability.
            # But since we have intervals, we can work with intervals.
            
            # Let's use a different approach: maintain the reachable positions as a set of intervals.
            # For each position y in [start_good, end_good], y is reachable if there is an interval [u, v] in reachable_intervals
            # such that u <= y - A and v >= y - B, and u <= v (which is always true).
            # This is equivalent to: y - B <= v and y - A >= u.
            # So y is reachable if there exists [u, v] such that u <= y - A and v >= y - B.
            # This means y is in [u + A, v + B].
            
            # So the set of reachable positions in the good interval is the union of [u + A, v + B] for all [u, v] in reachable_intervals,
            # intersected with [start_good, end_good].
            
            # Let's compute this union.
            candidate_intervals = []
            for (u, v) in reachable_intervals:
                # The interval [u, v] can reach [u+A, v+B]
                low = u + A
                high = v + B
                if low <= end_good and high >= start_good:
                    # Intersect with [start_good, end_good]
                    inter_low = max(low, start_good)
                    inter_high = min(high, end_good)
                    if inter_low <= inter_high:
                        candidate_intervals.append((inter_low, inter_high))
            
            # Merge overlapping intervals in candidate_intervals
            if not candidate_intervals:
                new_reachable = []
            else:
                candidate_intervals.sort()
                merged = []
                curr_start, curr_end = candidate_intervals[0]
                for i in range(1, len(candidate_intervals)):
                    next_start, next_end = candidate_intervals[i]
                    if next_start <= curr_end + 1:
                        curr_end = max(curr_end, next_end)
                    else:
                        merged.append((curr_start, curr_end))
                        curr_start, curr_end = next_start, next_end
                merged.append((curr_start, curr_end))
                new_reachable = merged
            
            # Now, check if any of these new reachable intervals is "stable" (contiguous of length >= B)
            # If so, all subsequent positions in the good interval are reachable.
            # We can then set the reachable set for the rest of the good interval to be a single interval.
            
            # Let's find the rightmost position in new_reachable that is part of a "stable" block.
            # A block is stable if its length >= B.
            # If we have a stable block ending at pos, then all positions from pos + 1 to end_good are reachable.
            
            stable_end = -1
            for (s, e) in new_reachable:
                if e - s + 1 >= B:
                    stable_end = e
                    break
            
            if stable_end != -1:
                # All positions from stable_end + 1 to end_good are reachable.
                # We need to add (stable_end + 1, end_good) to new_reachable if it's valid.
                if stable_end + 1 <= end_good:
                    # Check if this interval overlaps with the last interval in new_reachable
                    if new_reachable and new_reachable[-1][1] >= stable_end:
                        # Merge
                        last_s, last_e = new_reachable[-1]
                        new_reachable[-1] = (last_s, end_good)
                    else:
                        new_reachable.append((stable_end + 1, end_good))
            
            # Update reachable_intervals to be the new_reachable intervals within [start_good, end_good]
            # But we also need to keep reachable intervals that are beyond end_good?
            # No, because we are processing sequentially. The reachable intervals beyond end_good are not yet computed.
            # Actually, the reachable_intervals should be updated to only include positions up to end_good for now?
            # No, we need to keep all reachable positions. But positions beyond end_good are not yet determined.
            # We will determine them when we process the next good interval.
            # So we replace reachable_intervals with new_reachable.
            reachable_intervals = new_reachable
        
        # Now, we need to "jump" over the bad interval [L_bad, R_bad].
        # The bad interval makes all positions in [L_bad, R_bad] unreachable.
        # We need to compute which positions > R_bad are reachable from the current reachable_intervals.
        
        # A position y > R_bad is reachable if there exists x in reachable_intervals such that:
        # x + A <= y <= x + B
        # i.e., y - B <= x <= y - A
        
        # So y is reachable if there is an interval [u, v] in reachable_intervals such that:
        # u <= y - A and v >= y - B
        # This is the same condition as before, but now we are looking for y > R_bad.
        
        # Let's compute the new reachable intervals for positions > R_bad.
        # We are interested in positions up to the next bad interval or N.
        # But we don't know the next bad interval yet. We'll compute the reachable intervals and then filter them later.
        
        # Actually, we can compute the reachable intervals for all y > R_bad that can be reached from current reachable_intervals.
        # These will be the new reachable_intervals for the next step.
        
        next_candidate_intervals = []
        for (u, v) in reachable_intervals:
            # The interval [u, v] can reach [u+A, v+B]
            low = u + A
            high = v + B
            # We only care about positions > R_bad
            if high > R_bad:
                inter_low = max(low, R_bad + 1)
                inter_high = high
                if inter_low <= inter_high:
                    next_candidate_intervals.append((inter_low, inter_high))
        
        # Merge overlapping intervals
        if not next_candidate_intervals:
            reachable_intervals = []
        else:
            next_candidate_intervals.sort()
            merged = []
            curr_start, curr_end = next_candidate_intervals[0]
            for i in range(1, len(next_candidate_intervals)):
                next_start, next_end = next_candidate_intervals[i]
                if next_start <= curr_end + 1:
                    curr_end = max(curr_end, next_end)
                else:
                    merged.append((curr_start, curr_end))
                    curr_start, curr_end = next_start, next_end
            merged.append((curr_start, curr_end))
            reachable_intervals = merged
        
        prev_bad_end = R_bad

    # After processing all bad intervals, we have a final stretch of good squares from prev_bad_end + 1 to N.
    # We need to check if N is reachable.
    
    # Propagate reachability through the final good interval [prev_bad_end + 1, N]
    start_good = prev_bad_end + 1
    end_good = N
    
    if start_good <= end_good:
        candidate_intervals = []
        for (u, v) in reachable_intervals:
            low = u + A
            high = v + B
            if low <= end_good and high >= start_good:
                inter_low = max(low, start_good)
                inter_high = min(high, end_good)
                if inter_low <= inter_high:
                    candidate_intervals.append((inter_low, inter_high))
        
        if candidate_intervals:
            candidate_intervals.sort()
            merged = []
            curr_start, curr_end = candidate_intervals[0]
            for i in range(1, len(candidate_intervals)):
                next_start, next_end = candidate_intervals[i]
                if next_start <= curr_end + 1:
                    curr_end = max(curr_end, next_end)
                else:
                    merged.append((curr_start, curr_end))
                    curr_start, curr_end = next_start, next_end
            merged.append((curr_start, curr_end))
            
            # Check if N is in any of the merged intervals
            for (s, e) in merged:
                if s <= N <= e:
                    print("Yes")
                    return
                # Optimization: if we have a stable block, all subsequent positions are reachable
                if e - s + 1 >= B:
                    if N >= s:
                        print("Yes")
                        return
        
        # If no intervals, N is not reachable
        print("No")
    else:
        # No good interval at the end, check if N was already reachable
        # But N is always > prev_bad_end, so this case shouldn't happen if N > prev_bad_end.
        # If N <= prev_bad_end, then N is bad, so not reachable.
        # But the problem says R_i < N, so N is always good.
        # So start_good <= N always.
        print("No")

solve()