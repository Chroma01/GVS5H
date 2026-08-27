import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    P = list(map(int, input_data[1:]))
    
    # P is 1-indexed in the problem, but we'll use 0-indexed list for P
    # P[i] corresponds to the insertion position for number i+1
    # We process from N down to 1, so we look at P[N-1], P[N-2], ..., P[0]
    
    # Binary Indexed Tree (Fenwick Tree) to manage empty slots
    # bit[i] stores the sum of frequencies from index 1 to i
    # We use 1-based indexing for the BIT
    bit = [0] * (N + 1)
    
    # Initialize BIT: all positions are empty (value 1)
    # We can build the BIT in O(N)
    for i in range(1, N + 1):
        bit[i] += 1
        j = i + (i & (-i))
        if j <= N:
            bit[j] += bit[i]
            
    # Function to find the k-th empty slot using binary lifting on BIT
    def find_kth_empty(k):
        idx = 0
        current_sum = 0
        # Determine the highest power of 2 less than or equal to N
        bit_mask = 1
        while bit_mask <= N:
            bit_mask <<= 1
        bit_mask >>= 1
        
        while bit_mask > 0:
            t_idx = idx + bit_mask
            if t_idx <= N:
                if current_sum + bit[t_idx] < k:
                    idx = t_idx
                    current_sum += bit[t_idx]
            bit_mask >>= 1
            
        # The k-th empty slot is at idx + 1
        return idx + 1
    
    # Function to update the BIT: subtract 1 at position pos
    def update(pos, val):
        while pos <= N:
            bit[pos] += val
            pos += pos & (-pos)
            
    # Result array to store the final positions
    result = [0] * (N + 1)  # 1-indexed
    
    # Process from N down to 1
    # For number i (from N to 1), it was inserted at position P[i-1]
    # We need to find the P[i-1]-th empty slot
    for i in range(N, 0, -1):
        p_i = P[i-1]
        pos = find_kth_empty(p_i)
        result[pos] = i
        update(pos, -1)
        
    # Output the result from index 1 to N
    print(' '.join(map(str, result[1:])))

solve()