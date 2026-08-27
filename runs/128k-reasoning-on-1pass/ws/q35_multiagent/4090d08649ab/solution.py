import sys

def solve():
    input_data = sys.stdin.read().split()
    N = int(input_data[0])
    A = [int(x) for x in input_data[1:N+1]]
    
    # Part 1: Sum of |S_{L,R}| over all subarrays
    # Each element A[i] contributes as the first occurrence of its value
    # in subarrays starting after its previous occurrence and ending at or after i
    total_distinct = 0
    prev_occ = {}  # value -> last occurrence index (1-indexed)
    
    for i in range(N):
        val = A[i]
        pos = i + 1  # 1-indexed
        prev = prev_occ.get(val, 0)
        total_distinct += (pos - prev) * (N - pos + 1)
        prev_occ[val] = pos
    
    # Part 2: Sum of adjacent value pair counts over all subarrays
    # For fixed R, count of L where both v and v-1 are present = min(last_occ(v), last_occ(v-1))
    # We maintain the sum of these minimums efficiently
    last_occ = {}  # value -> last occurrence index (1-indexed)
    pair_sum = 0  # running sum of min(last_occ(v), last_occ(v-1)) for all v
    
    total_pairs = 0
    
    for i in range(N):
        val = A[i]
        pos = i + 1  # 1-indexed
        
        # When last_occ[val] changes, only two terms are affected:
        # min(last_occ(val), last_occ(val-1)) and min(last_occ(val+1), last_occ(val))
        if val in last_occ:
            old_val = last_occ[val]
            prev_val = last_occ.get(val - 1, 0)
            pair_sum -= min(old_val, prev_val)
            next_val = last_occ.get(val + 1, 0)
            pair_sum -= min(next_val, old_val)
        
        last_occ[val] = pos
        
        prev_val = last_occ.get(val - 1, 0)
        pair_sum += min(pos, prev_val)
        next_val = last_occ.get(val + 1, 0)
        pair_sum += min(next_val, pos)
        
        total_pairs += pair_sum
    
    print(total_distinct - total_pairs)

solve()