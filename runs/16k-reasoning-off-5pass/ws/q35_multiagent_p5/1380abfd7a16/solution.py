import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    P = [0] * (N + 1)
    for i in range(1, N + 1):
        P[i] = int(input_data[i])
    
    # Fenwick Tree (Binary Indexed Tree)
    # We'll use 1-indexed BIT of size N
    bit = [0] * (N + 1)
    
    def update(i, delta):
        """Add delta to element at index i (1-indexed)"""
        while i <= N:
            bit[i] += delta
            i += i & (-i)
    
    def query(i):
        """Return prefix sum from 1 to i"""
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s
    
    # Initialize BIT with 1s at all positions 1..N
    # We can do this efficiently by building the BIT in O(N)
    # But for simplicity and since N <= 5e5, O(N log N) initialization is fine
    for i in range(1, N + 1):
        update(i, 1)
    
    # Result array, 1-indexed for convenience
    result = [0] * (N + 1)
    
    # Process from N down to 1
    # For each i, find the P[i]-th available position
    def find_kth(k):
        """Find the smallest index idx such that query(idx) == k"""
        # Binary search on the BIT
        # We want the smallest idx where prefix_sum(idx) >= k
        # Since all values are 0 or 1, prefix_sum(idx) == k means exactly k ones up to idx
        
        # Binary lifting on BIT for O(log N)
        idx = 0
        current_sum = 0
        # Find the largest power of 2 <= N
        bit_mask = 1
        while bit_mask <= N:
            bit_mask <<= 1
        bit_mask >>= 1
        
        while bit_mask > 0:
            next_idx = idx + bit_mask
            if next_idx <= N and current_sum + bit[next_idx] < k:
                idx = next_idx
                current_sum += bit[idx]
            bit_mask >>= 1
        
        return idx + 1
    
    for i in range(N, 0, -1):
        pos = find_kth(P[i])
        result[pos] = i
        update(pos, -1)  # Mark this position as occupied
    
    # Output result[1..N]
    print(' '.join(map(str, result[1:])))

solve()