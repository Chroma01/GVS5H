import sys

# Increase recursion depth just in case, though we won't use recursion
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Term 1: Sum of number of distinct elements in all subarrays
    # We use a sweep-line with a Fenwick Tree (BIT)
    # For each position i (0-indexed), we want to count how many subarrays ending at i
    # have A[i] as the first occurrence of that value from the right.
    # This is equivalent to: i - prev_occurrence_index (where prev_occurrence_index is -1 if none)
    # But we need to sum this over all L for each R.
    # Standard approach:
    # Maintain a BIT that stores 1 at the current position of each distinct value.
    # When we move to index i with value A[i]:
    #   If A[i] appeared before at index prev, we remove the 1 at prev (update -1).
    #   We add 1 at i (update +1).
    #   The number of subarrays ending at i that contain A[i] as the rightmost occurrence
    #   (which effectively means A[i] is the representative for the distinct count)
    #   is the sum of the BIT from 0 to i.
    #   Actually, the standard trick is:
    #   The contribution of A[i] to the distinct count of subarrays ending at i is
    #   the number of L such that the first occurrence of A[i] in A[L..i] is at i.
    #   This is true for L in (prev_occurrence, i]. So there are i - prev_occurrence such L's.
    #   We can compute this directly without BIT if we just track prev occurrences.
    #   Let's do the direct O(N) approach for Term 1.
    
    # prev_occ[v] stores the last index (0-indexed) where value v was seen.
    prev_occ = [-1] * (N + 1)
    
    term1 = 0
    for i in range(N):
        val = A[i]
        last_pos = prev_occ[val]
        # The number of subarrays ending at i where A[i] is the first occurrence of val
        # is i - last_pos.
        term1 += (i - last_pos)
        prev_occ[val] = i

    # Term 2: Sum over v=1 to N-1 of (number of subarrays containing both v and v+1)
    # Count(both v and v+1) = Total - Count(missing v) - Count(missing v+1) + Count(missing both)
    # Total number of subarrays is N*(N+1)//2
    total_subarrays = N * (N + 1) // 2
    
    # Precompute positions for each value
    positions = [[] for _ in range(N + 1)]
    for i in range(N):
        positions[A[i]].append(i)
        
    def count_missing_subarrays(pos_list, n):
        """
        Given a sorted list of positions where a value appears,
        count the number of subarrays that do NOT contain this value.
        These are subarrays contained entirely within the gaps.
        Gaps are: [0, pos[0]-1], [pos[0]+1, pos[1]-1], ..., [pos[-1]+1, n-1]
        Length of a gap is (end - start + 1). Number of subarrays in a gap of length L is L*(L+1)//2.
        """
        if not pos_list:
            # If the value never appears, all subarrays are missing it.
            return total_subarrays
        
        count = 0
        prev = -1
        for p in pos_list:
            # Gap from prev+1 to p-1
            gap_len = p - prev - 1
            if gap_len > 0:
                count += gap_len * (gap_len + 1) // 2
            prev = p
        
        # Final gap from last_pos+1 to n-1
        gap_len = n - prev - 1
        if gap_len > 0:
            count += gap_len * (gap_len + 1) // 2
            
        return count

    term2 = 0
    for v in range(1, N):
        pos_v = positions[v]
        pos_v1 = positions[v + 1]
        
        # Count missing v
        missing_v = count_missing_subarrays(pos_v, N)
        # Count missing v+1
        missing_v1 = count_missing_subarrays(pos_v1, N)
        
        # Count missing both v and v+1
        # Merge the two sorted lists of positions
        # Since they are already sorted, we can merge them in linear time relative to their sizes
        merged = []
        i, j = 0, 0
        len_v = len(pos_v)
        len_v1 = len(pos_v1)
        while i < len_v and j < len_v1:
            if pos_v[i] < pos_v1[j]:
                merged.append(pos_v[i])
                i += 1
            else:
                merged.append(pos_v1[j])
                j += 1
        while i < len_v:
            merged.append(pos_v[i])
            i += 1
        while j < len_v1:
            merged.append(pos_v1[j])
            j += 1
            
        missing_both = count_missing_subarrays(merged, N)
        
        # Inclusion-Exclusion
        # Count(both) = Total - Count(missing v) - Count(missing v+1) + Count(missing both)
        count_both = total_subarrays - missing_v - missing_v1 + missing_both
        term2 += count_both

    ans = term1 - term2
    print(ans)

solve()