import sys
from functools import cmp_to_key
import bisect

# Increase recursion depth just in case
sys.setrecursionlimit(300005)

def solve():
    # Read all input from stdin at once
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        num_test_cases = int(next(iterator))
    except StopIteration:
        return

    results = []

    for _ in range(num_test_cases):
        try:
            N = int(next(iterator))
            A = []
            for _ in range(N):
                A.append(int(next(iterator)))
        except StopIteration:
            break

        # Identify distinct values and their properties
        last_pos = {}
        counts = {}
        
        for idx, val in enumerate(A):
            if val not in last_pos:
                last_pos[val] = idx
                counts[val] = 0
            last_pos[val] = idx
            counts[val] += 1
            
        distinct_values = list(counts.keys())
        m = len(distinct_values)
        
        # Precompute positions for each value
        positions = {val: [] for val in distinct_values}
        for idx, val in enumerate(A):
            positions[val].append(idx)
            
        # Define comparison function
        # We want to sort such that u comes before v if count(u before last[v]) > count(v before last[u])
        def compare(u, v):
            # Count u's before last_pos[v]
            # positions[u] is sorted, so we can use bisect_right
            cnt_u_before_v = bisect.bisect_right(positions[u], last_pos[v] - 1)
            # Count v's before last_pos[u]
            cnt_v_before_u = bisect.bisect_right(positions[v], last_pos[u] - 1)
            
            if cnt_u_before_v > cnt_v_before_u:
                return -1 
            elif cnt_u_before_v < cnt_v_before_u:
                return 1  
            else:
                return 0

        distinct_values.sort(key=cmp_to_key(compare))
        
        rank_map = {val: i for i, val in enumerate(distinct_values)}
        
        # Calculate Base Cost
        # Cost to gather v is (last_pos[v] - counts[v])
        base_swaps = 0
        for val in distinct_values:
            base_swaps += (last_pos[val] - counts[val])
        
        total_ops = base_swaps + m
        
        # Calculate Gain using BIT
        # We want to sum over i from 0 to N-1: count of v such that last_pos[v] > i and rank(v) > rank(A[i])
        # We iterate i from N-1 down to 0.
        # At step i, we need BIT to contain all v with last_pos[v] > i.
        # When moving from i+1 to i, we add v with last_pos[v] == i+1.
        
        bit = [0] * (m + 1)
        
        def update_bit(idx, val):
            while idx <= m:
                bit[idx] += val
                idx += idx & (-idx)
                
        def query_bit(idx):
            s = 0
            while idx > 0:
                s += bit[idx]
                idx -= idx & (-idx)
            return s
            
        # Group values by their last position
        buckets = [[] for _ in range(N + 2)]
        for v in distinct_values:
            buckets[last_pos[v]].append(v)
            
        total_gain = 0
        
        # Iterate i from N-1 down to 0
        for i in range(N - 1, -1, -1):
            # Before processing i, we need BIT to contain all v with last_pos[v] > i.
            # Currently, BIT contains v with last_pos[v] > i+1 (from previous iterations).
            # We need to add v with last_pos[v] == i+1.
            
            if i + 1 < len(buckets):
                for v in buckets[i+1]:
                    update_bit(rank_map[v] + 1, 1)
            
            x = A[i]
            r = rank_map[x] + 1
            
            # Query count of v with rank > r
            count_greater = query_bit(m) - query_bit(r)
            total_gain += count_greater
            
        total_ops = base_swaps + m - total_gain
        results.append(str(total_ops))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()