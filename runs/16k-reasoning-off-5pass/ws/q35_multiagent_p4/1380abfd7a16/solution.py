import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    P = list(map(int, input_data[1:N+1]))
    
    # We'll use a Fenwick tree (BIT) to track empty positions.
    # Initially, all positions 1..N are empty.
    # BIT[i] stores the sum of frequencies from index 1 to i.
    # We want to find the k-th empty position efficiently.
    
    # Fenwick tree operations
    bit = [0] * (N + 1)
    
    def update(i, delta):
        """Add delta to element at index i (1-indexed)."""
        while i <= N:
            bit[i] += delta
            i += i & (-i)
    
    def query(i):
        """Return sum from 1 to i."""
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s
    
    # Initialize: all positions 1..N are empty, so each has value 1.
    for i in range(1, N + 1):
        update(i, 1)
    
    # Result array (1-indexed, we'll use 0-indexed internally but positions are 1-indexed)
    result = [0] * (N + 1)  # result[pos] = value at position pos (1-indexed)
    
    # Process from i = N down to 1
    # P[i-1] is the position where i was inserted (1-indexed)
    for i in range(N, 0, -1):
        p = P[i-1]  # the p-th empty slot to fill
        
        # Find the smallest index pos such that query(pos) == p
        # This is the p-th empty position.
        # We can use binary lifting on the BIT for O(log N) search.
        
        # Binary lifting to find the p-th empty slot
        pos = 0
        current_sum = 0
        bit_mask = 1 << (N.bit_length() - 1)  # largest power of 2 <= N
        
        while bit_mask > 0:
            next_pos = pos + bit_mask
            if next_pos <= N:
                new_sum = current_sum + bit[next_pos]
                if new_sum < p:
                    pos = next_pos
                    current_sum = new_sum
            bit_mask >>= 1
        
        # pos is now the largest index such that query(pos) < p
        # So the p-th empty position is pos + 1
        target_pos = pos + 1
        
        result[target_pos] = i
        
        # Mark this position as occupied (decrement by 1)
        update(target_pos, -1)
    
    # Output the result from position 1 to N
    print(' '.join(str(result[i]) for i in range(1, N + 1)))

solve()