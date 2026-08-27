import sys
from bisect import bisect_left, bisect_right

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Precompute positions for each value (1-indexed positions)
    # Values are in range 1 to N
    pos = [[] for _ in range(N + 1)]
    for i, a in enumerate(A):
        pos[a].append(i + 1)  # Store 1-based index

    total_sum = 0
    total_pairs = N * (N + 1) // 2

    # Iterate over each value v from 1 to N
    # We want to count pairs (L, R) such that:
    # 1. The subarray A[L..R] contains at least one occurrence of v
    # 2. The subarray A[L..R] contains NO occurrence of v-1
    # This count contributes 1 to f(L,R) for each such pair.
    
    for v in range(1, N + 1):
        if v == 1:
            # v-1 = 0, which never appears in A (values are >= 1)
            # So condition 2 is always true.
            # We just need to count pairs (L,R) that contain at least one v.
            
            p_list = pos[v]
            if not p_list:
                # v doesn't appear in A, so no subarray contains it
                continue
            
            # Calculate number of subarrays that DO NOT contain v
            # These are subarrays lying entirely within gaps between occurrences of v
            prev = 0
            gap_sum = 0
            for p in p_list:
                length = p - prev - 1
                if length > 0:
                    gap_sum += length * (length + 1) // 2
                prev = p
            
            # Gap after the last occurrence
            length = N + 1 - prev - 1
            if length > 0:
                gap_sum += length * (length + 1) // 2
            
            count_v = total_pairs - gap_sum
            total_sum += count_v
            
        else:
            # v-1 appears in A (possibly)
            occ_prev = pos[v-1]
            
            # The valid intervals [L,R] must not contain any occurrence of v-1.
            # This means [L,R] must be strictly inside one of the intervals defined by consecutive occurrences of v-1.
            # Let bounds be [0] + occ_prev + [N+1]
            # The intervals are (bounds[j], bounds[j+1]) for j in 0..len(bounds)-2
            # The actual indices available are bounds[j]+1 to bounds[j+1]-1
            
            bounds = [0] + occ_prev + [N + 1]
            count_v = 0
            p_list = pos[v]
            
            for j in range(len(bounds) - 1):
                left_bound = bounds[j] + 1
                right_bound = bounds[j+1] - 1
                
                if left_bound > right_bound:
                    continue
                
                len_interval = right_bound - left_bound + 1
                total_in_interval = len_interval * (len_interval + 1) // 2
                
                # Find occurrences of v within [left_bound, right_bound]
                # Use binary search on p_list
                idx_start = bisect_left(p_list, left_bound)
                idx_end = bisect_right(p_list, right_bound)
                
                occ_v_in_interval = p_list[idx_start:idx_end]
                
                # Calculate number of subarrays in this interval that DO NOT contain v
                # These are subarrays lying in gaps between consecutive occurrences of v within this interval
                # The "gaps" are defined by the occurrences of v, plus the boundaries of the interval
                
                prev_occ = bounds[j]  # This is the index of the last v-1 occurrence (or 0)
                gap_sum_interval = 0
                
                for occ in occ_v_in_interval:
                    length = occ - prev_occ - 1
                    if length > 0:
                        gap_sum_interval += length * (length + 1) // 2
                    prev_occ = occ
                
                # Gap after the last occurrence of v in this interval, up to the next v-1 occurrence
                length = bounds[j+1] - prev_occ - 1
                if length > 0:
                    gap_sum_interval += length * (length + 1) // 2
                
                # Number of subarrays in this interval that DO contain v
                count_v += (total_in_interval - gap_sum_interval)
            
            total_sum += count_v

    print(total_sum)

if __name__ == '__main__':
    solve()