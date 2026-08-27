import sys

# Increase recursion depth just in case, though we use iterative BIT
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        P = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Fenwick Tree (Binary Indexed Tree) implementation
    # We initialize the BIT with 1s at all positions 1 to N.
    # bit[i] will store the sum of frequencies in the range covered by node i.
    # Initially, every position is "empty" (count = 1).
    # When a position is filled, we update it with -1.
    # query(x) will then return the number of empty slots in range [1, x].
    
    bit = [0] * (N + 1)
    
    # Initialize BIT with 1s for all positions 1..N
    # This can be done in O(N).
    # bit[i] stores sum of range [i - (i&-i) + 1, i]
    # Initially all values are 1, so bit[i] should be (i & -i).
    for i in range(1, N + 1):
        bit[i] = i & (-i)
    
    # We inline the update and find_kth logic for performance, 
    # but keep them as functions for clarity in this block.
    # update(idx, delta): Adds delta to element at idx (1-based).
    # find_kth(k): Finds the smallest index idx such that query(idx) >= k using binary lifting.
    
    def update(idx, delta):
        """Adds delta to element at idx (1-based)."""
        while idx <= N:
            bit[idx] += delta
            idx += idx & (-idx)
            
    def find_kth(k):
        """
        Finds the smallest index idx such that query(idx) >= k using binary lifting.
        This runs in O(log N).
        """
        idx = 0
        current_sum = 0
        # Determine the highest power of 2 less than or equal to N
        # bit_mask starts at the largest power of 2 <= N
        if N == 0: return 0
        bit_mask = 1 << (N.bit_length() - 1)
        
        while bit_mask > 0:
            t_idx = idx + bit_mask
            if t_idx <= N and current_sum + bit[t_idx] < k:
                idx = t_idx
                current_sum += bit[idx]
            bit_mask >>= 1
        
        return idx + 1

    # Array to store the final position of each number.
    # result_pos[i] will store the final 1-based position of number i.
    # We need an array of size N+1.
    final_positions = [0] * (N + 1)
    
    # Process numbers from N down to 1
    # For number i (where i goes from N to 1):
    # The operation was: insert i at P[i-1] (1-based position).
    # In the final array, i will be placed at the P[i-1]-th *empty* slot.
    # Why? Because all numbers j > i have already been placed (processed in reverse).
    # The slots occupied by j > i are "filled". We need the P[i-1]-th slot that is NOT filled.
    
    # P is 0-indexed in our list, but the problem uses 1-based indexing for positions.
    # P[i] corresponds to the position for number (i+1).
    # So for number 'val', the target position is P[val-1].
    
    for i in range(N, 0, -1):
        p_val = P[i-1] # 1-based position requested for number i
        
        # Find the p_val-th empty slot
        pos = find_kth(p_val)
        
        # Place number i at pos
        final_positions[pos] = i
        update(pos, -1) # Mark this position as occupied (decrement count from 1 to 0)
    
    # Construct the output
    # final_positions is 1-based, so slice from 1 to N
    output = [str(final_positions[i]) for i in range(1, N + 1)]
    print(" ".join(output))

if __name__ == '__main__':
    solve()