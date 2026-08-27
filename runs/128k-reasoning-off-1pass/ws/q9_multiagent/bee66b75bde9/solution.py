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
    except StopIteration:
        return

    # Initialize constraints
    # L[i] and R[i] for rows 1..N (using 0-based index internally: 0..N-1)
    # A[j] and B[j] for cols 1..N (using 0-based index internally: 0..N-1)
    # Since N can be up to 10^9, we use dictionaries for sparse constraints.
    # However, for the greedy check, we need to iterate j from N down to 1.
    # But N is large. We must coordinate compress or realize that cap(j) is non-zero only for j in specific ranges.
    # Actually, cap(j) is the count of rows i such that L[i] <= j <= R'[i].
    # The function cap(j) is a sum of indicator functions. It is piecewise constant.
    # The values of j where cap(j) changes are L[i] and R'[i]+1.
    # Also A[j] and B[j] are defined by input points.
    # We need to check the condition for all j in 1..N.
    # Since N is large, we cannot iterate all j.
    # However, note that A[j] and B[j] are only non-trivial (non-zero or non-N) at specific columns?
    # No, A[j] comes from 'B' at (x, y) -> A[y-1] = max(A[y-1], x).
    # B[j] comes from 'W' at (x, y) -> B[y-1] = min(B[y-1], x-1).
    # For columns not mentioned, A[j]=0, B[j]=N.
    # Similarly for rows.
    # The critical observation is that we only need to check the condition at points where the "tightness" changes.
    # But the greedy logic requires checking every step?
    # Actually, if cap(j) is constant and A[j], B[j] are constant over an interval, the recurrence is linear.
    # f(j) = min(C, f(j+1) + K).
    # This can be solved in O(1) per interval.
    
    # Let's collect all critical x and y coordinates.
    # Rows involved: X coordinates from input.
    # Cols involved: Y coordinates from input.
    # Also we need to consider the boundaries.
    
    # Step 1: Parse and initialize sparse constraints
    # We will use dictionaries for L, R, A, B.
    # Default values: L[i]=0, R[i]=N, A[j]=0, B[j]=N.
    
    L = {} # row index -> min black prefix
    R = {} # row index -> max black prefix
    
    A = {} # col index -> min black prefix
    B = {} # col index -> max black prefix
    
    # We also need to track which rows/cols have constraints to iterate efficiently.
    # But for the greedy part, we need to process j from N down to 1.
    # Since N is large, we identify intervals of j where A[j], B[j], and cap(j) are constant.
    
    # First, populate L, R, A, B from input
    for _ in range(M):
        x = int(next(iterator))
        y = int(next(iterator))
        c = next(iterator)
        
        # Convert to 0-based
        r_idx = x - 1
        c_idx = y - 1
        
        if c == 'B':
            # Row x must have at least y blacks
            if r_idx not in L or y > L[r_idx]:
                L[r_idx] = y
            # Col y must have at least x blacks
            if c_idx not in A or x > A[c_idx]:
                A[c_idx] = x
        else: # 'W'
            # Row x must have at most y-1 blacks
            if r_idx not in R or y - 1 < R[r_idx]:
                R[r_idx] = y - 1
            # Col y must have at most x-1 blacks
            if c_idx not in B or x - 1 < B[c_idx]:
                B[c_idx] = x - 1
                
    # Step 2: Refine R[i] using column upper bounds
    # For each col j, if B[j] < N, then for all i > B[j], R[i] <= j.
    # (Using 1-based logic for clarity: if B[j] < i, then R[i] <= j-1)
    # In 0-based: if B[j] < i, then R[i] <= j.
    # Wait, let's re-verify the 0-based mapping.
    # Input: W at (x, y) (1-based). Row x (0-based: x-1), Col y (0-based: y-1).
    # Condition: Row x has at most y-1 blacks. So R[x-1] = min(..., y-1).
    # Condition: Col y has at most x-1 blacks. So B[y-1] = min(..., x-1).
    # The constraint derived: If B[j] < i (where i is row index 0-based), then R[i] <= j.
    # Proof: B[j] is the max allowed black cells in col j. So rows > B[j] must have 0 in col j?
    # No. Col j has black cells in rows 0..B[j]. So rows B[j]+1..N-1 must have WHITE in col j.
    # If row i has WHITE in col j, then its black prefix length R[i] must be < j+1 (since col index is j).
    # So R[i] <= j.
    # Correct.
    
    # We need to apply this constraint.
    # For each j where B[j] is defined, we update R[i] for i > B[j].
    # Since N is large, we cannot iterate all i.
    # However, R[i] is only non-trivial for i in L.keys() or where we need to check consistency.
    # Actually, we need to check if L[i] <= R[i] for all i.
    # And we need to compute cap(j) = count(i | L[i] <= j <= R'[i]).
    # The set of i where L[i] > 0 is small. For i not in L, L[i]=0.
    # The set of i where R[i] < N is small (from 'W' inputs).
    # For i not in R, R[i]=N.
    # So most i have L[i]=0, R[i]=N.
    # The constraint R[i] <= j for i > B[j] will affect many i.
    # Specifically, for a fixed j, all i in [B[j]+1, N-1] get R[i] = min(R[i], j).
    # This effectively sets an upper bound on R[i] for a suffix of rows.
    # Let's store these updates.
    # We can represent the updates as: for each j, we have a constraint R[i] <= j for i > B[j].
    # This is equivalent to: R[i] <= min_{j: B[j] < i} (j).
    # Let U[i] = min_{j: B[j] < i} (j). If no such j, U[i] = N.
    # We need to compute U[i] efficiently.
    # The condition B[j] < i means j > B[j] is not the condition. It is i > B[j].
    # So for a given i, we look at all j such that B[j] < i.
    # We want min(j) among those.
    # Let's collect all pairs (B[j], j) for all j in B.
    # Sort them by B[j].
    # Then for a given i, we want min(j) for all pairs with B[j] < i.
    # As i increases, the set of valid j grows. The minimum j can only decrease.
    # So U[i] is non-increasing with i.
    # We can compute U[i] for all relevant i.
    # Relevant i are those where L[i] > 0 (since if L[i]=0, 0 <= U[i] is always true)
    # OR where we need to compute cap(j).
    # Actually, to compute cap(j), we need to know for each j, how many i satisfy L[i] <= j <= R'[i].
    # R'[i] = min(R[i], U[i]).
    # Since U[i] is non-increasing, and R[i] is mostly N, R'[i] will be determined by U[i] for large i.
    # Let's compute U[i] for all i that matter.
    # The "events" for U[i] are at i = B[j] + 1.
    # At i = B[j] + 1, the constraint j becomes active.
    # So U[i] = min(U[i-1], j) for i = B[j] + 1.
    # We can compute U[i] for all i in the set of interesting coordinates.
    # Interesting coordinates for i: {B[j] + 1 for all j in B} U {X coordinates}.
    # Let's collect these points, sort them, and compute U[i] at these points.
    # Between points, U[i] is constant.
    
    # Similarly, we need to check L[i] <= R'[i].
    # And compute cap(j).
    
    # Let's gather all critical row indices:
    # 1. X coordinates from input.
    # 2. B[j] + 1 for all j in B.
    # Sort unique critical row indices: P_rows.
    # Also include 0 and N.
    
    critical_rows = set()
    for r in L:
        critical_rows.add(r)
    for j in B:
        val = B[j] + 1
        if val < N:
            critical_rows.add(val)
        else:
            # If B[j] >= N-1, then constraint applies to no rows (since i < N)
            pass
            
    critical_rows.add(0)
    critical_rows.add(N)
    sorted_rows = sorted(list(critical_rows))
    
    # Compute U[i] at these points.
    # U[i] = min(j) for all j such that B[j] < i.
    # We can iterate through sorted_rows and maintain the min j seen so far for B[j] < current_i.
    # But B[j] < i is the condition.
    # Let's create a list of events: (threshold, j).
    # Event: at i = B[j] + 1, we introduce constraint j.
    # So for i >= B[j] + 1, U[i] <= j.
    # We want U[i] = min(j) for all active constraints.
    
    events = []
    for j, val in B.items():
        if val < N:
            events.append((val + 1, j))
    
    # Sort events by threshold (i)
    events.sort(key=lambda x: x[0])
    
    # Compute U[i] for each critical row
    # U[i] is constant between critical rows?
    # Yes, because the set of active constraints {j | B[j] < i} only changes when i crosses B[j]+1.
    
    U_map = {} # i -> U[i]
    
    current_min_j = N
    event_idx = 0
    num_events = len(events)
    
    for r in sorted_rows:
        # Activate all events with threshold <= r
        while event_idx < num_events and events[event_idx][0] <= r:
            current_min_j = min(current_min_j, events[event_idx][1])
            event_idx += 1
        
        U_map[r] = current_min_j
        
    # Now we have U[i] for critical rows.
    # For any i, R'[i] = min(R[i], U[i]).
    # If i is not in critical_rows, U[i] = U_map[prev_critical] (since U is non-increasing? No, U is non-increasing).
    # Wait, U[i] = min_{j: B[j] < i} j. As i increases, the set grows, so min decreases.
    # So U[i] is non-increasing.
    # Thus U[i] for i in (sorted_rows[k], sorted_rows[k+1]) is U_map[sorted_rows[k+1]]?
    # No. U[i] is determined by constraints with B[j] < i.
    # If i is between two critical points, say r1 < i < r2.
    # The set of j with B[j] < i is the same as for r1?
    # Critical points are B[j]+1.
    # If i > B[j], then j is active.
    # If i <= B[j], j is not active.
    # So the set of active j changes exactly at i = B[j] + 1.
    # So for i in [r_k, r_{k+1}-1], the set of active j is constant?
    # Yes, because no B[j]+1 falls in (r_k, r_{k+1}).
    # So U[i] is constant in [r_k, r_{k+1}-1].
    # And U[r_k] is computed correctly.
    # So for any i, U[i] = U_map[r_k] where r_k is the largest critical row <= i.
    
    # Now we need to check L[i] <= R'[i] for all i.
    # R'[i] = min(R[i], U[i]).
    # If i not in L, L[i]=0. 0 <= R'[i] is always true.
    # If i in L, we check L[i] <= min(R[i], U[i]).
    # We only need to check i in L.
    # For i in L, find U[i] using binary search on sorted_rows.
    
    # Also need to check A[j] <= B[j] for all j.
    # And A[j] <= B[j] is implied by the existence of solution?
    # We should check explicitly.
    
    for j in A:
        if j not in B or A[j] > B[j]:
            print("No")
            return
    for j in B:
        if j not in A and B[j] < 0: # Should not happen as B[j] >= 0
            pass
            
    # Check L[i] <= R'[i]
    # We need to find U[i] for each i in L.
    # Since U is non-increasing, we can use bisect_right to find the position.
    # We want largest r in sorted_rows such that r <= i.
    # Then U[i] = U_map[r].
    
    import bisect
    
    for r, min_val in L.items():
        # Find U[r]
        # bisect_right returns insertion point.
        # We want index of element <= r.
        idx = bisect.bisect_right(sorted_rows, r) - 1
        if idx < 0:
            # Should not happen as 0 is in sorted_rows
            U_val = N
        else:
            U_val = U_map[sorted_rows[idx]]
        
        R_prime = min(R.get(r, N), U_val)
        if min_val > R_prime:
            print("No")
            return

    # Now we need to check the greedy condition for j from N-1 down to 0.
    # We need to compute cap(j) = count(i | L[i] <= j <= R'[i]).
    # Since N is large, we cannot iterate j.
    # However, cap(j) is non-zero only for j in [min(L), max(R')].
    # And cap(j) is piecewise constant.
    # The values of j where cap(j) changes are L[i] and R'[i]+1.
    # Let's collect all such j.
    # Also A[j] and B[j] change at input Y coordinates.
    # So we need critical columns:
    # 1. Y coordinates from input.
    # 2. L[i] for all i.
    # 3. R'[i] + 1 for all i.
    
    critical_cols = set()
    for c in A:
        critical_cols.add(c)
    for c in B:
        critical_cols.add(c)
    for r in L:
        critical_cols.add(L[r])
        # R'[r] depends on U[r] which depends on B.
        # We need R'[r].
        # Compute R'[r] for all r in L.
        # We already computed U[r] above.
        R_prime_r = min(R.get(r, N), U_map[sorted_rows[bisect.bisect_right(sorted_rows, r)-1]])
        critical_cols.add(R_prime_r + 1)
        critical_cols.add(R_prime_r) # Just in case
        
    # Also add 0 and N
    critical_cols.add(0)
    critical_cols.add(N)
    
    sorted_cols = sorted(list(critical_cols))
    
    # We need to evaluate the recurrence:
    # f(j) = min(B[j], f(j+1) + cap(j))
    # Check f(j) >= A[j] and f(j) >= f(j+1).
    # We process intervals of j where A[j], B[j], cap(j) are constant.
    # Let's build the values for these intervals.
    
    # Precompute A_val[j] and B_val[j] for critical cols.
    # For j not in A, A_val = 0.
    # For j not in B, B_val = N.
    
    # Precompute cap(j) for critical cols.
    # cap(j) = count(i | L[i] <= j <= R'[i]).
    # This is the number of rows i such that j is in [L[i], R'[i]].
    # This is equivalent to: count of intervals [L[i], R'[i]] covering j.
    # We can use a sweep-line or difference array on critical cols.
    # Since critical_cols is sorted, we can iterate.
    
    # Let's create a list of intervals [L[i], R'[i]] for all i in L.
    # For i not in L, L[i]=0, R'[i]=N (since U[i]=N, R[i]=N).
    # But wait, if i not in L, L[i]=0.
    # Does i not in L contribute to cap(j)?
    # Yes, if 0 <= j <= R'[i].
    # R'[i] for i not in L:
    # U[i] is determined by B.
    # If i not in L, L[i]=0.
    # We need R'[i] for all i?
    # Actually, cap(j) = count(i | L[i] <= j <= R'[i]).
    # If i not in L, L[i]=0. So condition is 0 <= j <= R'[i].
    # R'[i] = min(R[i], U[i]).
    # R[i] = N (default).
    # U[i] = min_{k: B[k] < i} k.
    # So for i not in L, we still need R'[i].
    # But R'[i] might be small if U[i] is small.
    # So we need to consider ALL i from 0 to N-1?
    # No, N is large.
    # However, U[i] is constant on intervals defined by critical_rows.
    # And R[i] is constant (N) except for i in R.
    # So R'[i] is piecewise constant.
    # We can compute cap(j) by summing contributions from each interval of i.
    # But cap(j) is a function of j.
    # We need to check the condition for all j.
    # The condition is: f(j) >= A[j] and f(j) <= B[j] (implied by recurrence) and f(j) >= f(j+1).
    # Actually, the recurrence ensures f(j) <= B[j] and f(j) >= f(j+1) if we check bounds.
    # The only hard constraint is f(j) >= A[j].
    # And we need to ensure that the constructed f(j) is realizable.
    # The realizability condition is f(j) - f(j+1) <= cap(j).
    # Our recurrence: f(j) = min(B[j], f(j+1) + cap(j)).
    # This ensures f(j) - f(j+1) <= cap(j).
    # So if we satisfy f(j) >= A[j] for all j, we are good.
    
    # So we need to check if there exists a sequence f(j) satisfying:
    # 1. f(N) = 0 (base case, actually f(N) corresponds to j=N, which is 0-based index N-1? No, j goes 0..N-1. f(N) is 0).
    # 2. f(j) <= B[j]
    # 3. f(j) >= A[j]
    # 4. f(j) <= f(j+1) + cap(j)
    # 5. f(j) >= f(j+1) (non-increasing)
    
    # We process j from N-1 down to 0.
    # f(j) = min(B[j], f(j+1) + cap(j)).
    # Then check f(j) >= A[j] and f(j) >= f(j+1).
    # If at any point f(j) < A[j] or f(j) < f(j+1), return No.
    
    # We need to evaluate this for all j.
    # But we can jump over intervals where A[j], B[j], cap(j) are constant.
    # Let's define the intervals.
    # Critical points for j: sorted_cols.
    # In each interval [c_k, c_{k+1}-1], A, B, cap are constant.
    # Let A_val, B_val, cap_val be the values in this interval.
    # Recurrence: f(j) = min(B_val, f(j+1) + cap_val).
    # Let g(k) be the value of f at the start of the interval (j = c_k).
    # We know f(c_{k+1}) from the previous step (end of next interval).
    # Wait, we process backwards.
    # Let's denote the intervals as I_0, I_1, ... I_m where I_k = [c_k, c_{k+1}-1].
    # We process from last interval to first.
    # For the last interval [c_m, N-1], we know f(N)=0.
    # We compute f(c_m).
    # Then move to previous interval.
    
    # However, cap(j) might be 0 for large j.
    # If cap(j)=0, then f(j) = min(B[j], f(j+1)).
    # If B[j] < f(j+1), then f(j) = B[j].
    # If B[j] >= f(j+1), then f(j) = f(j+1).
    # So f(j) is non-increasing.
    
    # Let's implement the sweep.
    
    # First, compute cap(j) for all critical cols.
    # cap(j) = count(i | L[i] <= j <= R'[i]).
    # We can compute this using a difference array on the critical cols.
    # But we need cap(j) for all j in the intervals.
    # Since cap(j) is constant in [c_k, c_{k+1}-1], we just need cap(c_k).
    # How to compute cap(c_k) efficiently?
    # cap(j) = sum_{i} [L[i] <= j <= R'[i]].
    # This is the number of intervals covering j.
    # We can use a sweep-line on the intervals [L[i], R'[i]].
    # Events: (L[i], +1), (R'[i]+1, -1).
    # Sort events by coordinate.
    # Iterate through sorted_cols.
    
    # Collect intervals
    intervals = []
    for r in range(N):
        # L[r] and R'[r]
        # If r not in L, L[r]=0.
        # If r not in R, R[r]=N.
        # U[r] needs to be computed.
        # U[r] is constant on intervals of critical_rows.
        # We can compute U[r] for all r? No, N is large.
        # But we only need cap(j) for j in critical_cols.
        # And cap(j) depends on all i.
        # However, U[r] is determined by B.
        # U[r] = min_{k: B[k] < r} k.
        # This is non-increasing in r.
        # Also R[r] is N for most r.
        # So R'[r] = U[r] for most r.
        # The intervals [L[r], R'[r]] are [0, U[r]] for r not in L.
        # For r in L, [L[r], min(R[r], U[r])].
        
        # We can group r by U[r].
        # U[r] is constant on [sorted_rows[k], sorted_rows[k+1]-1].
        # Let's iterate through these blocks.
        pass

    # Let's build the events for cap(j).
    # We need to know U[r] for each r.
    # U[r] is piecewise constant.
    # Let's create a list of (start_r, end_r, U_val).
    # Then for each block, we have a range of r with same U_val.
    # For r in this block:
    #   If r in L: L_val = L[r], R_val = min(R[r], U_val). Interval [L_val, R_val].
    #   Else: L_val = 0, R_val = U_val. Interval [0, U_val].
    # We add events for these intervals.
    
    # Since N is large, we cannot iterate all r.
    # But the blocks are defined by critical_rows.
    # Number of blocks is O(M).
    # So we can iterate blocks.
    
    # Build blocks
    blocks = []
    prev_r = 0
    for r in sorted_rows:
        if r > prev_r:
            # Block [prev_r, r-1]
            # Compute U_val for this block.
            # U_val is U_map[prev_r] (since U is non-increasing and constant between critical points? No, U is non-increasing, but constant between B[j]+1).
            # Yes, U[i] is constant for i in [B[j]+1, B[k]+1-1].
            # So U_val = U_map[prev_r].
            U_val = U_map[prev_r]
            blocks.append((prev_r, r-1, U_val))
        prev_r = r
    # Last block
    if prev_r < N:
        U_val = U_map[prev_r]
        blocks.append((prev_r, N-1, U_val))
        
    # Now generate events
    # Event: (pos, type) where type +1 for start, -1 for end+1.
    # We need to query cap(j) at specific j (critical_cols).
    # We can sort events and sweep.
    
    events = []
    for start_r, end_r, U_val in blocks:
        if start_r > end_r:
            continue
        if start_r in L:
            L_val = L[start_r]
            R_val = min(R.get(start_r, N), U_val)
            if L_val <= R_val:
                events.append((L_val, 1))
                events.append((R_val + 1, -1))
        else:
            L_val = 0
            R_val = U_val
            if L_val <= R_val:
                events.append((L_val, 1))
                events.append((R_val + 1, -1))
                
    events.sort(key=lambda x: x[0])
    
    # Now sweep to compute cap(j) for j in critical_cols
    # We need cap(j) for j in sorted_cols.
    # We can iterate through sorted_cols and update current_cap.
    
    current_cap = 0
    event_idx = 0
    num_events = len(events)
    
    # Map for A and B values
    # A[j] = A.get(j, 0)
    # B[j] = B.get(j, N)
    
    # We need to process intervals [c_k, c_{k+1}-1].
    # For each interval, we need cap_val = cap(c_k).
    # And A_val, B_val.
    
    # Check consistency
    f_next = 0 # f(N) = 0
    
    # We need to handle the case where critical_cols might not cover all j?
    # No, we added 0 and N.
    # But we need to check f(j) >= A[j] for ALL j.
    # If A[j] is 0 for most j, it's fine.
    # If A[j] > 0, then j must be in A.keys().
    # So we only need to check j in A.keys() and the boundaries?
    # Actually, if A[j] > 0, then j is in critical_cols.
    # If A[j] = 0, then f(j) >= 0 is always true.
    # So we only need to check j in A.keys().
    # But we also need to ensure f(j) >= f(j+1).
    # If f(j) drops below f(j+1), it's invalid.
    # This can happen even if A[j]=0.
    # So we need to check the recurrence for all intervals.
    
    # Let's iterate through sorted_cols.
    # For each interval [c_k, c_{k+1}-1]:
    #   Determine A_val, B_val, cap_val.
    #   Update f_next from f_current (which is f(c_{k+1})) to f(c_k).
    #   Wait, we process backwards.
    #   Let's store the intervals and process backwards.
    
    intervals_check = []
    for k in range(len(sorted_cols) - 1):
        c_k = sorted_cols[k]
        c_next = sorted_cols[k+1]
        if c_k >= c_next:
            continue
            
        # Determine values in [c_k, c_next - 1]
        # A_val
        A_val = A.get(c_k, 0)
        # B_val
        B_val = B.get(c_k, N)
        # cap_val
        # Update current_cap to c_k
        while event_idx < num_events and events[event_idx][0] <= c_k:
            current_cap += events[event_idx][1]
            event_idx += 1
        cap_val = current_cap
        
        intervals_check.append((c_k, c_next, A_val, B_val, cap_val))
        
    # Process backwards
    f_next = 0
    for k in range(len(intervals_check) - 1, -1, -1):
        c_k, c_next, A_val, B_val, cap_val = intervals_check[k]
        
        # We need to compute f(c_k) from f(c_next)
        # f(c_k) = min(B_val, f(c_next) + cap_val * (c_next - c_k)) ?
        # No. The recurrence is f(j) = min(B[j], f(j+1) + cap(j)).
        # If cap(j) is constant C and B[j] is constant B in the interval.
        # Then f(j) = min(B, f(j+1) + C).
        # This is applied for each step j from c_next-1 down to c_k.
        # Let x = f(c_next).
        # f(c_next-1) = min(B, x + C)
        # f(c_next-2) = min(B, min(B, x+C) + C) = min(B, x + 2C)
        # ...
        # f(c_k) = min(B, x + (c_next - c_k) * C)
        # BUT, this is only true if B >= x + k*C for all k.
        # Actually, min(B, min(B, ...)) is just min(B, x + k*C) as long as x + k*C <= B.
        # If x + k*C > B, then it becomes B.
        # So f(c_k) = min(B, x + (c_next - c_k) * C).
        # Wait, is it possible that f(j) hits B and stays B?
        # Yes. If f(j+1) + C >= B, then f(j) = B.
        # Then f(j-1) = min(B, B + C) = B.
        # So yes, f(c_k) = min(B, f(c_next) + (c_next - c_k) * C).
        
        # However, we must also check the condition f(j) >= f(j+1).
        # f(c_k) >= f(c_next) is guaranteed if C >= 0.
        # But we need f(j) >= A[j] for all j in the interval.
        # The minimum value of f(j) in the interval is f(c_next) (since f is non-increasing).
        # Wait, f(j) = min(B, f(j+1) + C).
        # If C > 0, f(j) >= f(j+1).
        # If C = 0, f(j) = min(B, f(j+1)). So f(j) <= f(j+1).
        # But we require f(j) >= f(j+1) (non-increasing sequence).
        # So if C=0, we must have f(j) = f(j+1) (since f(j) <= f(j+1) and f(j) >= f(j+1)).
        # This implies f(j) = f(j+1) = min(B, f(j+1)).
        # So if C=0, we need f(j+1) <= B.
        # If f(j+1) > B, then f(j) = B < f(j+1), which violates non-increasing.
        # So if C=0 and f(j+1) > B, impossible.
        # Also we need f(j) >= A[j].
        # Since f(j) is non-increasing, the minimum is f(c_next).
        # So we need f(c_next) >= A_val.
        # Wait, if C > 0, f(j) increases as j decreases.
        # So min is f(c_next).
        # So we need f(c_next) >= A_val.
        # If C=0, f(j) is constant (if f(j+1) <= B) or drops to B.
        # If f(j+1) > B, then f(j)=B < f(j+1), invalid.
        # So if C=0, we need f(j+1) <= B.
        # And then f(j) = f(j+1).
        # So min is f(c_next).
        # So in all cases, we need f(c_next) >= A_val.
        # And we need to compute f(c_k).
        
        # Compute f(c_k)
        # If cap_val > 0:
        #   f_curr = min(B_val, f_next + (c_next - c_k) * cap_val)
        # If cap_val == 0:
        #   if f_next > B_val:
        #       return No (violation of non-increasing)
        #   f_curr = min(B_val, f_next) # which is f_next if f_next <= B_val
        
        # Actually, the formula min(B, f_next + len * C) works for C=0 too?
        # If C=0, min(B, f_next). If f_next > B, result B.
        # But we need f_curr >= f_next.
        # If f_next > B, f_curr = B < f_next. Invalid.
        # So we must check f_curr >= f_next.
        
        length = c_next - c_k
        if cap_val > 0:
            f_curr = min(B_val, f_next + length * cap_val)
        else:
            if f_next > B_val:
                print("No")
                return
            f_curr = f_next # min(B, f_next) is f_next since f_next <= B
        
        # Check non-increasing
        if f_curr < f_next:
            print("No")
            return
            
        # Check lower bound A_val
        # We need f(j) >= A_val for all j in [c_k, c_next-1].
        # Since f is non-increasing, min is f(c_next) = f_next.
        # So we need f_next >= A_val.
        if f_next < A_val:
            print("No")
            return
            
        f_next = f_curr
        
    print("Yes")

solve()