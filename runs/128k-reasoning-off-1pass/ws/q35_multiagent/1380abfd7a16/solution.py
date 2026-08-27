import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    P = list(map(int, input_data[1:N+1]))
    
    # We'll use a Fenwick tree (BIT) to track empty slots.
    # Initially, all N slots are empty, so we have 1s at positions 1..N.
    # bit[i] stores the sum of frequencies from index (i - (i&-i) + 1) to i.
    
    bit = [0] * (N + 1)
    
    def update(i, delta):
        """Add delta to element at position i (1-indexed)."""
        while i <= N:
            bit[i] += delta
            i += i & (-i)
    
    def query(i):
        """Return prefix sum from 1 to i."""
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s
    
    # Initialize BIT: all positions 1..N have value 1 (empty)
    for i in range(1, N + 1):
        update(i, 1)
    
    # Result array, 1-indexed for convenience, will store the final array.
    result = [0] * (N + 1)
    
    # Process from N down to 1
    # For number i, it was inserted at position P[i-1] (0-indexed in P list)
    # We need to find the P[i-1]-th empty slot.
    
    for i in range(N, 0, -1):
        target = P[i-1]  # The position (1-indexed) where i was inserted
        
        # Find the smallest index idx such that query(idx) == target
        # This is the target-th empty slot.
        # We can use binary lifting on the BIT for O(log N) search.
        
        idx = 0
        current_sum = 0
        # Start from the highest power of 2 less than or equal to N
        bit_mask = 1 << (N.bit_length() - 1)
        
        while bit_mask > 0:
            next_idx = idx + bit_mask
            if next_idx <= N and current_sum + bit[next_idx] < target:
                idx = next_idx
                current_sum += bit[next_idx]
            bit_mask >>= bit_mask
        
        # The target-th empty slot is at idx + 1
        target_idx = idx + 1
        
        # Place i at target_idx
        result[target_idx] = i
        
        # Mark this slot as filled (decrement by 1)
        update(target_idx, -1)
    
    # Output the result from index 1 to N
    print(' '.join(map(str, result[1:])))

solve()