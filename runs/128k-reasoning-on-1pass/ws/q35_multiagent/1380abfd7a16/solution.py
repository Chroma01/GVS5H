import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        P = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return
    
    # Binary Indexed Tree (BIT) array, 1-indexed
    # tree[i] stores the sum of frequencies in the range [i - (i&-i) + 1, i]
    tree = [0] * (N + 1)
    
    # Initialize BIT for an array of all 1s (all slots empty initially)
    # For an array of all 1s, tree[i] = i & -i
    for i in range(1, N + 1):
        tree[i] = i & -i
        
    ans = [0] * (N + 1)
    
    # Precompute the starting bit_mask for binary lifting
    # This is the largest power of 2 less than or equal to N
    bit_mask = 1 << (N.bit_length() - 1)
    
    # Process operations in reverse order from N down to 1
    for i in range(N, 0, -1):
        k = P[i-1]
        
        # Find the position of the k-th empty slot using binary lifting on BIT
        # We want to find the smallest index 'pos' such that sum(1..pos) >= k
        # The loop finds the largest index 'idx' such that sum(1..idx) < k
        idx = 0
        current_sum = 0
        bm = bit_mask
        
        while bm > 0:
            next_idx = idx + bm
            if next_idx <= N and current_sum + tree[next_idx] < k:
                idx = next_idx
                current_sum += tree[next_idx]
            bm >>= 1
            
        pos = idx + 1
        ans[pos] = i
        
        # Update BIT: decrement the count at pos (mark slot as occupied)
        # This effectively removes the slot from the set of empty slots
        while pos <= N:
            tree[pos] -= 1
            pos += pos & (-pos)
            
    # Print the result array (1-indexed, so skip index 0)
    print(*(ans[1:]))

if __name__ == '__main__':
    solve()