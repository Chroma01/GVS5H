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
    except StopIteration:
        return

    bad_intervals = []
    for _ in range(M):
        L = int(next(iterator))
        R = int(next(iterator))
        bad_intervals.append((L, R))

    # If N is 1, we are already there (but constraints say N >= 2)
    if N == 1:
        print("Yes")
        return

    # Construct good intervals
    # Bad intervals are sorted and disjoint by constraints
    # Good intervals are the gaps between bad intervals, plus [1, L1-1] and [RM+1, N]
    
    good_intervals = []
    
    # Start from 1
    current_start = 1
    
    for (L, R) in bad_intervals:
        # The interval [current_start, L-1] is good if current_start <= L-1
        if current_start <= L - 1:
            good_intervals.append((current_start, L - 1))
        # Move current_start to R+1
        current_start = R + 1
    
    # Add the last good interval if any
    if current_start <= N:
        good_intervals.append((current_start, N))
    
    # If there are no good intervals, we can't even start (but 1 is always good since Li > 1)
    if not good_intervals:
        print("No")
        return
    
    # Check if square 1 is in the first good interval
    # Since Li > 1, the first good interval starts at 1.
    if good_intervals[0][0] != 1:
        # This should not happen given constraints, but for safety
        print("No")
        return

    # We will maintain the range of reachable positions in the current good interval
    # Let [L_reach, R_reach] be the range of reachable positions in the current good interval.
    # Initially, for the first good interval, we start at 1.
    
    # For each good interval, we compute the reachable range.
    # The reachable range in a good interval [S, E] given the previous reachable range [L_prev, R_prev]
    # is computed as follows:
    # 1. Positions reachable by a single jump from the previous interval:
    #    [max(S, L_prev + A), min(E, R_prev + B)]
    # 2. Within the current good interval, we can make multiple jumps.
    #    If the reachable range has length >= B - A, then we can reach all positions up to E.
    #    Otherwise, we expand the range iteratively.
    
    # Initialize reachable range for the first good interval
    # We start at 1, so initially reachable = {1}
    # But we need to compute the range of reachable positions in the first good interval.
    
    # Let's process each good interval
    # For the first good interval, the "previous" reachable range is just {1} at position 1.
    # But 1 is in the first good interval. So we start with reachable = [1, 1] in the first good interval.
    
    # However, we can only jump from 1 to positions in [1+A, 1+B] within the first good interval.
    # So the initial reachable range in the first good interval is [1, 1] (we are at 1),
    # and then we expand by making jumps.
    
    # General algorithm for a good interval [S, E] with previous reachable range [L_prev, R_prev]:
    #   L_init = max(S, L_prev + A)
    #   R_init = min(E, R_prev + B)
    #   If L_init > R_init, then no position in this interval is reachable -> return No
    #   If R_init == E, then we can reach the end of this interval.
    #   If R_init < E, we can make further jumps within the interval.
    #   The reachable range expands to [L_init + A, R_init + B], clipped to [S, E].
    #   We repeat this until R_init == E or the range becomes empty or stabilizes.
    #   Optimization: if R_init - L_init >= B - A, then we can reach E if E >= L_init + A.
    
    # For the first good interval, we can consider the "previous" reachable range as [1, 1] at position 1.
    # But 1 is in the first good interval. So we start with reachable = [1, 1].
    # Then we expand: L_init = max(S, 1 + A), R_init = min(E, 1 + B).
    # But wait, we are already at 1, so 1 is reachable. Then we can jump to [1+A, 1+B].
    # So the reachable range in the first good interval is [1, min(E, 1+B)] if we consider staying at 1?
    # No, the problem says "move from square 1 to square N". So we start at 1, and we need to make jumps.
    # But we can also consider that 1 is reachable, and then we can jump from 1.
    
    # Let's redefine: for each good interval, we compute the range of reachable positions.
    # For the first good interval [S1, E1], we start with reachable = [1, 1] (since we start at 1).
    # Then we expand: 
    #   L_new = max(S1, L_reach + A)
    #   R_new = min(E1, R_reach + B)
    #   If L_new > R_new, then no further positions are reachable.
    #   Else, update L_reach = L_new, R_reach = R_new.
    #   Repeat until R_reach == E1 or L_new > R_new.
    
    # But this can be slow if E1 - S1 is large.
    # Optimization: if R_reach - L_reach >= B - A, then we can reach E1 if E1 >= L_reach + A.
    
    # Let's implement this with optimization.
    
    # For the first good interval, we start with reachable = [1, 1]
    L_reach = 1
    R_reach = 1
    
    for (S, E) in good_intervals:
        # If the current reachable range is empty, break
        if L_reach > R_reach:
            print("No")
            return
        
        # If the current reachable range is entirely before S, we need to jump to this interval
        # The positions in [S, E] reachable from [L_reach, R_reach] are:
        #   [max(S, L_reach + A), min(E, R_reach + B)]
        
        # But if the current reachable range overlaps with [S, E], we need to handle it.
        # Actually, the good intervals are disjoint and sorted. So the previous reachable range is in the previous good interval, which ends before S.
        # So L_reach and R_reach are <= previous E, which is < S.
        # So we can always compute the new reachable range as:
        
        L_new = max(S, L_reach + A)
        R_new = min(E, R_reach + B)
        
        if L_new > R_new:
            print("No")
            return
        
        # Now, within [S, E], we can make further jumps.
        # We need to expand the reachable range until it stabilizes or reaches E.
        
        # Optimization: if R_new - L_new >= B - A, then we can reach E if E >= L_new + A.
        # Because the range will expand by at least B-A each step, and if it's large enough, it will cover E.
        
        if R_new < E:
            if R_new - L_new >= B - A:
                # We can reach E if E >= L_new + A
                if E >= L_new + A:
                    R_new = E
                else:
                    # We cannot reach E, but we can reach up to R_new + B? No, we need to check.
                    # Actually, if R_new - L_new >= B - A, then the next range is [L_new+A, R_new+B],
                    # which has length R_new+B - (L_new+A) = (R_new-L_new) + (B-A) >= B.
                    # So the length increases. We can reach E if E is within the expanded range.
                    # But we already checked E >= L_new + A. If not, then we cannot reach E.
                    # So we set R_new to min(E, R_new + B) but we need to ensure the range is non-empty.
                    # Actually, if E < L_new + A, then we cannot reach E.
                    # So we leave R_new as is, and it will be < E.
                    pass
            else:
                # Expand once
                L_next = max(S, L_new + A)
                R_next = min(E, R_new + B)
                
                if L_next > R_next:
                    # Cannot expand further
                    pass
                else:
                    L_new = L_next
                    R_new = R_next
                    
                    # Check again with optimization
                    if R_new < E and R_new - L_new >= B - A:
                        if E >= L_new + A:
                            R_new = E
        
        # Update the reachable range for the next interval
        L_reach = L_new
        R_reach = R_new
        
        # If we reached E, we can continue to the next interval
        # If not, we still continue, but the reachable range is [L_reach, R_reach]
    
    # After processing all good intervals, check if we reached N
    # The last good interval ends at N (since we added [current_start, N] if current_start <= N)
    # So if R_reach == N, then we can reach N.
    # But wait, the last good interval might not end at N if N is in a bad interval? 
    # No, by construction, the last good interval ends at N if N is good.
    # And N is good because R_i < N for all i.
    
    if R_reach == N:
        print("Yes")
    else:
        # Check if N is in the last good interval and if R_reach >= N
        # Actually, the last good interval ends at N, so if R_reach == N, we are good.
        # But what if the last good interval is [S, N] and R_reach < N?
        # Then we cannot reach N.
        print("No")

solve()