import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    P = [int(x) for x in data[1:]]
    
    # We'll use a Fenwick Tree (BIT) to manage available positions.
    # Initially, all positions 1..N are available (value 1).
    # We need to support:
    # 1. Find the k-th available position (binary lifting on BIT)
    # 2. Update a position to 0 (mark as occupied)
    
    # BIT array (1-indexed, size N+1)
    bit = [0] * (N + 1)
    
    def update(i, delta):
        """Add delta to element at index i (1-indexed)."""
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
    
    # Initialize BIT: set all positions 1..N to 1
    # We can do this by updating each position, but that's O(N log N).
    # Alternatively, we can build it in O(N).
    # For simplicity and since N <= 5*10^5, O(N log N) init is fine.
    for i in range(1, N + 1):
        update(i, 1)
    
    # Result array (1-indexed conceptually, but we'll use 0-indexed list)
    result = [0] * N
    
    # Process from N down to 1
    # P is 0-indexed in our list, so P[i-1] corresponds to the insertion position for number i
    for i in range(N, 0, -1):
        p_i = P[i - 1]  # The position (1-indexed) where i was inserted
        
        # Find the p_i-th available position using binary lifting on BIT
        # We want the smallest index pos such that query(pos) == p_i
        # Since all values are 0 or 1, query(pos) gives the count of available positions in [1, pos]
        
        # Binary lifting on BIT to find the k-th one
        pos = 0
        current_sum = 0
        # Start from the highest power of 2 less than or equal to N
        bit_mask = 1 << (N.bit_length() - 1)
        
        while bit_mask > 0:
            next_pos = pos + bit_mask
            if next_pos <= N:
                if current_sum + bit[next_pos] < p_i:
                    pos = next_pos
                    current_sum += bit[pos]
            bit_mask >>= 1
        
        # The answer is pos + 1
        target_pos = pos + 1
        
        # Assign the number i to this position (0-indexed: target_pos - 1)
        result[target_pos - 1] = i
        
        # Mark this position as occupied (set to 0)
        update(target_pos, -1)
    
    # Output the result
    print(' '.join(map(str, result)))

solve()