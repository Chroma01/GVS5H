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

    # 1-based indexing for logic, but 0-based for list access
    # pos[v] will store list of 0-based indices where value v appears
    # Values are 1 to N. We use size N+2 to be safe.
    pos = [[] for _ in range(N + 2)]
    for i, x in enumerate(A):
        pos[x].append(i)

    total_ans = 0

    # Iterate over each value v that can start a block
    # A block starts at v if v is present and (v-1) is NOT present
    for v in range(1, N + 1):
        # We need to count subarrays [L, R] such that:
        # 1. v is in A[L..R]
        # 2. (v-1) is NOT in A[L..R]
        
        # Condition 2 implies the subarray must lie entirely within a "gap" 
        # formed by the occurrences of (v-1).
        
        if v == 1:
            # For v=1, we just need subarrays containing 1.
            # The "gap" constraint is trivial (no v-1 to avoid).
            # We consider the whole array [0, N-1] as the single gap.
            gaps = [(0, N - 1)]
        else:
            # Get positions of v-1
            prev_pos = pos[v - 1]
            if not prev_pos:
                # If v-1 never appears, the whole array is one gap
                gaps = [(0, N - 1)]
            else:
                # Construct gaps between occurrences of v-1
                # Gap 1: [0, prev_pos[0] - 1]
                # Gap k: [prev_pos[k-1] + 1, prev_pos[k] - 1]
                # Gap last: [prev_pos[-1] + 1, N - 1]
                gaps = []
                if prev_pos[0] > 0:
                    gaps.append((0, prev_pos[0] - 1))
                
                for k in range(len(prev_pos) - 1):
                    start = prev_pos[k] + 1
                    end = prev_pos[k+1] - 1
                    if start <= end:
                        gaps.append((start, end))
                
                last = prev_pos[-1] + 1
                if last <= N - 1:
                    gaps.append((last, N - 1))
        
        # For each gap, count subarrays containing at least one v
        # Count = Total_subarrays_in_gap - Subarrays_avoiding_v_in_gap
        
        # Pre-fetch positions of v for binary search
        curr_pos = pos[v]
        
        for (gap_start, gap_end) in gaps:
            # Total subarrays in [gap_start, gap_end]
            length = gap_end - gap_start + 1
            total_sub = length * (length + 1) // 2
            
            # Find occurrences of v within [gap_start, gap_end]
            # Using bisect to find indices in curr_pos
            # We want indices i such that gap_start <= curr_pos[i] <= gap_end
            
            # Find first index >= gap_start
            idx_start = bisect_left(curr_pos, gap_start)
            # Find first index > gap_end
            idx_end = bisect_right(curr_pos, gap_end)
            
            # The occurrences are curr_pos[idx_start : idx_end]
            # If no occurrences, all subarrays avoid v
            if idx_start >= idx_end:
                avoiding_sub = total_sub
            else:
                # Calculate subarrays avoiding v
                # These are subarrays strictly between occurrences of v
                # Segments: [gap_start, curr_pos[idx_start]-1], 
                #            [curr_pos[idx_start]+1, curr_pos[idx_start+1]-1], ...
                #            [curr_pos[idx_end-1]+1, gap_end]
                
                avoiding_sub = 0
                
                # First segment before first v
                first_v = curr_pos[idx_start]
                len1 = first_v - gap_start
                if len1 > 0:
                    avoiding_sub += len1 * (len1 + 1) // 2
                
                # Middle segments between v's
                for k in range(idx_start, idx_end - 1):
                    u1 = curr_pos[k]
                    u2 = curr_pos[k+1]
                    len_mid = u2 - u1 - 1
                    if len_mid > 0:
                        avoiding_sub += len_mid * (len_mid + 1) // 2
                
                # Last segment after last v
                last_v = curr_pos[idx_end - 1]
                len2 = gap_end - last_v
                if len2 > 0:
                    avoiding_sub += len2 * (len2 + 1) // 2
            
            total_ans += (total_sub - avoiding_sub)

    print(total_ans)

if __name__ == '__main__':
    solve()