import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        P = [0] * (N + 1)
        for i in range(1, N + 1):
            P[i] = int(next(iterator))
    except StopIteration:
        return
    
    # Fenwick Tree (Binary Indexed Tree) implementation
    # We need to find the k-th empty slot.
    # Initially, all N slots are empty (value 1).
    # When a slot is filled, we update it to 0.
    # We use binary lifting on the BIT to find the index with a specific prefix sum.
    
    bit = [0] * (N + 1)
    
    # Initialize BIT with 1s at all positions in O(N)
    # bit[i] stores sum of frequencies from (i - (i&-i) + 1) to i
    # Since all are 1, bit[i] = i & (-i)
    for i in range(1, N + 1):
        bit[i] = i & (-i)
        
    result = [0] * (N + 1)
    
    # Process from N down to 1
    for i in range(N, 0, -1):
        target_pos = P[i]
        
        # Find the smallest index `idx` such that sum(1..idx) >= target_pos
        # Using binary lifting on BIT
        idx = 0
        current_sum = 0
        
        # Start from the highest power of 2 less than or equal to N
        # We can compute this dynamically. 
        # N.bit_length() gives the number of bits required to represent N.
        # 1 << (N.bit_length() - 1) is the largest power of 2 <= N.
        if N > 0:
            bit_mask = 1 << (N.bit_length() - 1)
        else:
            bit_mask = 0
            
        while bit_mask > 0:
            t_idx = idx + bit_mask
            if t_idx <= N and current_sum + bit[t_idx] < target_pos:
                idx = t_idx
                current_sum += bit[t_idx]
            bit_mask >>= 1
            
        # The answer is idx + 1 because we want the position where prefix sum becomes target_pos
        final_idx = idx + 1
        result[final_idx] = i
        
        # Update BIT: set position final_idx to 0 (subtract 1)
        # Standard update function
        update_idx = final_idx
        while update_idx <= N:
            bit[update_idx] -= 1
            update_idx += update_idx & (-update_idx)
        
    # Print result from index 1 to N
    print(*(result[1:]))

if __name__ == '__main__':
    solve()