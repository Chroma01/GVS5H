import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    try:
        T = int(next(iterator))
    except StopIteration:
        return

    results = []

    for _ in range(T):
        try:
            N = int(next(iterator))
            A = next(iterator)
            B = next(iterator)
        except StopIteration:
            break

        # Count pieces
        count_A = A.count('1')
        count_B = B.count('1')

        if count_A < count_B:
            results.append("-1")
            continue

        # Extract positions (1-indexed)
        A_pos = [i + 1 for i, c in enumerate(A) if c == '1']
        B_pos = [i + 1 for i, c in enumerate(B) if c == '1']
        
        M = len(A_pos)
        K = len(B_pos)
        
        # Binary search for the minimum max displacement D
        low = 0
        high = N
        ans = -1
        
        # Precompute B_pos for faster access if needed, but list is fine
        # B_pos is sorted
        
        def check(D):
            # We need to assign t_j in B_pos to each a_j in A_pos
            # such that t_1 <= t_2 <= ... <= t_M
            # and |a_j - t_j| <= D for all j
            # and {t_1, ..., t_M} covers all B_pos
            
            # Greedy strategy:
            # For each piece j, pick the smallest valid t_j >= t_{j-1}
            # Then verify coverage.
            
            last_t = -1 # Since positions are >= 1, -1 is safe lower bound
            
            # We also need to track which B_pos elements are covered.
            # Since we pick t_j in increasing order, we can just check if
            # the set of picked t_j includes all B_pos.
            # However, simply picking smallest valid might skip some B_pos if they are not "forced".
            # But wait: if we pick the smallest valid t_j >= last_t, we are minimizing t_j.
            # This leaves more room for subsequent pieces to cover larger B_pos values?
            # Actually, to cover B_pos, we want to ensure that for every b in B_pos,
            # there is some t_j == b.
            
            # Let's use a pointer for B_pos coverage.
            b_ptr = 0
            picked_t = []
            
            for j in range(M):
                a_j = A_pos[j]
                # Valid range for t_j: [a_j - D, a_j + D]
                # Also t_j >= last_t
                min_val = max(a_j - D, last_t)
                max_val = a_j + D
                
                if min_val > max_val:
                    return False
                
                # Find smallest b in B_pos such that b >= min_val and b <= max_val
                # Since B_pos is sorted, we can search.
                # We need b >= min_val.
                
                # Binary search or linear scan?
                # Since we iterate j, and min_val increases, we can maintain a pointer?
                # Not necessarily, because min_val depends on last_t which depends on previous picks.
                # But B_pos is small enough? N up to 10^6. O(N log N) total is fine.
                
                # Use bisect to find the first element >= min_val
                import bisect
                idx = bisect.bisect_left(B_pos, min_val)
                
                if idx >= K:
                    return False
                
                candidate = B_pos[idx]
                if candidate > max_val:
                    return False
                
                t_j = candidate
                picked_t.append(t_j)
                last_t = t_j
                
                # Mark covered B_pos elements
                # All B_pos elements <= t_j are potentially covered if they were not covered before?
                # No, we need to check if they are IN picked_t.
                # But we are building picked_t.
                # Let's just check coverage at the end?
                # Checking coverage at the end is O(M + K).
                # But we can do it incrementally to fail early?
                # Actually, just collecting picked_t and checking at the end is simpler and correct.
                
            # Check if all B_pos are in picked_t
            # Since picked_t is sorted and B_pos is sorted, we can merge/check
            b_ptr = 0
            for t in picked_t:
                while b_ptr < K and B_pos[b_ptr] < t:
                    return False
                if b_ptr < K and B_pos[b_ptr] == t:
                    b_ptr += 1
            
            return b_ptr == K

        # Optimization: The check function is O(M log K) or O(M) with pointer.
        # With bisect, it's O(M log K).
        # Total complexity O(N log N * log N) might be tight for 10^6?
        # Sum of N is 10^6. So O(N log^2 N) is acceptable.
        
        # Let's optimize check to O(M) using two pointers if possible.
        # But bisect is fast enough in Python for 10^6 total N?
        # Let's try to implement a linear scan within check if possible.
        # However, min_val jumps. Bisect is safer.
        
        # Re-define check with bisect
        import bisect
        
        def check_optimized(D):
            last_t = -1
            picked_t = []
            
            # To avoid creating a huge list, we can just track coverage
            # But we need to ensure t_j >= last_t.
            
            # We can iterate through B_pos to find candidates.
            # For each A_pos[j], we need smallest B_pos[k] >= max(a_j - D, last_t)
            # and <= a_j + D.
            
            # Since last_t increases, the search start index in B_pos also non-decreases?
            # Yes, because min_val = max(a_j - D, last_t).
            # last_t is non-decreasing. a_j - D might decrease?
            # A_pos is sorted, so a_j increases. a_j - D increases.
            # So min_val is non-decreasing.
            # Thus, the index in B_pos we start searching from is non-decreasing.
            
            b_idx = 0
            K = len(B_pos)
            
            for j in range(M):
                a_j = A_pos[j]
                min_val = max(a_j - D, last_t)
                max_val = a_j + D
                
                # Advance b_idx to first element >= min_val
                while b_idx < K and B_pos[b_idx] < min_val:
                    b_idx += 1
                
                if b_idx >= K:
                    return False
                
                candidate = B_pos[b_idx]
                if candidate > max_val:
                    return False
                
                t_j = candidate
                picked_t.append(t_j) # Keep for coverage check? Or check on fly?
                last_t = t_j
                
                # We can't easily check coverage on the fly because we might skip B_pos elements
                # that are covered by later pieces? No, t_j are non-decreasing.
                # If we pick t_j, we cover t_j.
                # We need to ensure every B_pos element is picked at least once.
                # Since we pick the smallest valid t_j, we might skip some B_pos elements
                # if they are not the smallest valid.
                # Example: B_pos = [2, 5], A_pos = [3, 3], D=2.
                # j=0: a_0=3. Range [1, 5]. min_val=1. Smallest B>=1 is 2. Pick 2.
                # j=1: a_1=3. Range [1, 5]. min_val=2 (last_t=2). Smallest B>=2 is 2. Pick 2.
                # Picked: [2, 2]. B_pos [2, 5] not covered.
                # So we MUST check coverage at the end.
                
            # Check coverage
            b_ptr = 0
            for t in picked_t:
                while b_ptr < K and B_pos[b_ptr] < t:
                    return False
                if b_ptr < K and B_pos[b_ptr] == t:
                    b_ptr += 1
            
            return b_ptr == K

        # Binary Search
        low = 0
        high = N
        ans = -1
        
        while low <= high:
            mid = (low + high) // 2
            if check_optimized(mid):
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
                
        results.append(str(ans))

    print('\n'.join(results))

solve()