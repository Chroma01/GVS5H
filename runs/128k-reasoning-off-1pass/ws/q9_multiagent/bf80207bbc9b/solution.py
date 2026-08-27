import sys
from collections import Counter

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Read grid rows and convert to integers
    # Each row is a string of '0' and '1'.
    # We map the string index 0 (leftmost) to bit W-1 (MSB)
    # and string index W-1 (rightmost) to bit 0 (LSB).
    # This ensures consistent bit manipulation.
    rows = []
    for _ in range(H):
        s = next(iterator)
        val = 0
        for char in s:
            val = (val << 1) | int(char)
        rows.append(val)

    # Precompute cost function: cost[p] = min(p, W - p)
    # This represents the minimum number of 1s in a row given the column flips,
    # assuming we optimally choose to flip the row or not.
    # If the row has p ones after column flips, we can flip the row to get W-p ones.
    # We take the minimum.
    cost = [min(p, W - p) for p in range(W + 1)]

    # Count frequency of each unique row pattern to handle large H efficiently
    row_counts = Counter(rows)
    
    # Helper to count set bits (popcount)
    def count_set_bits(n):
        c = 0
        while n:
            c += 1
            n &= n - 1
        return c

    # Helper to check if k-th bit is set (where k=0 is LSB)
    def has_bit(n, k):
        return (n >> k) & 1

    # Initialize data structures
    # current_pop_counts[p]: number of rows such that popcount(R ^ C) == p
    # where C is the current column flip mask.
    current_pop_counts = [0] * (W + 1)
    
    # bit_set[k][p]: number of rows such that popcount(R ^ C) == p AND the k-th bit of R is 1.
    # This allows us to quickly determine how many rows will have their popcount increase or decrease
    # when we flip the k-th bit of C.
    bit_set = [[0] * (W + 1) for _ in range(W)]
    
    # Initial state: C = 0 (no column flips)
    for r_val, count in row_counts.items():
        p = count_set_bits(r_val)
        current_pop_counts[p] += count
        for k in range(W):
            if has_bit(r_val, k):
                bit_set[k][p] += count

    # Calculate initial total cost for C=0
    total_cost = 0
    for p in range(W + 1):
        total_cost += current_pop_counts[p] * cost[p]
    
    min_total_cost = total_cost
    current_C = 0
    
    # Precompute the bit to flip for each step in Gray Code sequence
    # Gray code for n bits: g(i) = i ^ (i >> 1)
    # The bit that changes from i to i+1 is the position of the lowest set bit in i+1.
    num_masks = 1 << W
    flip_bit_at_step = [0] * (num_masks - 1)
    for i in range(num_masks - 1):
        step_val = i + 1
        # Find index of lowest set bit (0-indexed)
        flip_bit_at_step[i] = step_val.bit_length() - 1

    # Iterate through Gray Code
    # We start at C=0, then iterate 2^W - 1 steps to cover all 2^W masks.
    for i in range(num_masks - 1):
        k = flip_bit_at_step[i]
        
        # Determine direction based on current C's k-th bit
        # If current_C has bit k set (1):
        #   For rows with R_k=1: (R^C)_k is 0 -> becomes 1. Popcount increases by 1.
        #   For rows with R_k=0: (R^C)_k is 1 -> becomes 0. Popcount decreases by 1.
        # If current_C has bit k unset (0):
        #   For rows with R_k=1: (R^C)_k is 1 -> becomes 0. Popcount decreases by 1.
        #   For rows with R_k=0: (R^C)_k is 0 -> becomes 1. Popcount increases by 1.
        
        if (current_C >> k) & 1:
            # C_k is 1
            # Case 1: R_k=1. Current popcount p -> p+1.
            # These are tracked in bit_set[k][p].
            for p in range(W): 
                cnt = bit_set[k][p]
                if cnt > 0:
                    total_cost += cnt * (cost[p+1] - cost[p])
                    bit_set[k][p+1] += cnt
                    bit_set[k][p] -= cnt
            
            # Case 2: R_k=0. Current popcount p -> p-1.
            # Count is total rows with popcount p minus those with R_k=1.
            for p in range(1, W+1):
                cnt = current_pop_counts[p] - bit_set[k][p]
                if cnt > 0:
                    total_cost += cnt * (cost[p-1] - cost[p])
                    current_pop_counts[p-1] += cnt
                    current_pop_counts[p] -= cnt
                
        else:
            # C_k is 0
            # Case 1: R_k=1. Current popcount p -> p-1.
            for p in range(1, W+1):
                cnt = bit_set[k][p]
                if cnt > 0:
                    total_cost += cnt * (cost[p-1] - cost[p])
                    current_pop_counts[p-1] += cnt
                    current_pop_counts[p] -= cnt
                    bit_set[k][p-1] += cnt
                    bit_set[k][p] -= cnt
            
            # Case 2: R_k=0. Current popcount p -> p+1.
            for p in range(W):
                cnt = current_pop_counts[p] - bit_set[k][p]
                if cnt > 0:
                    total_cost += cnt * (cost[p+1] - cost[p])
                    current_pop_counts[p+1] += cnt
                    current_pop_counts[p] -= cnt
                    bit_set[k][p+1] += cnt
                    bit_set[k][p] -= cnt
        
        # Update current_C
        current_C ^= (1 << k)
        
        if total_cost < min_total_cost:
            min_total_cost = total_cost

    print(min_total_cost)

if __name__ == '__main__':
    solve()