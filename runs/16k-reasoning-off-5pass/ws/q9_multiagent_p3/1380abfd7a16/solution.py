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
        P = []
        for _ in range(N):
            P.append(int(next(iterator)))
    except StopIteration:
        return

    # P is 0-indexed in our list, but problem uses 1-based indexing for positions.
    # P[i] corresponds to the insertion position for number i+1.
    # Let's store P such that P[i] is the position for number i+1.
    # Actually, let's just keep P as is: P[0] is for 1, P[1] is for 2, ..., P[N-1] is for N.
    
    # We will process numbers from N down to 1.
    # For number i (where i goes from N down to 1), its insertion position in the forward pass
    # was P[i-1]. In the reverse pass, we need to find the (P[i-1])-th empty slot.
    
    # Fenwick Tree (Binary Indexed Tree) to manage empty slots.
    # Initially, all N positions are empty (value 1).
    # We need to support:
    # 1. Update: set a position to 0 (occupied).
    # 2. Query: find the smallest index idx such that sum(1..idx) == k.
    
    # BIT array (1-indexed)
    bit = [0] * (N + 1)
    
    # Initialize BIT with 1s at all positions 1..N
    # We can do this by adding 1 to each index, or building in O(N).
    # Building in O(N) is better.
    # bit[i] stores sum of frequencies from (i - (i&-i) + 1) to i.
    # Initially, frequency at every index j is 1.
    # So bit[i] = i & -i (sum of 1s in range covered by i).
    for i in range(1, N + 1):
        bit[i] = i & -i

    # Result array (1-indexed logic, but we'll use 0-indexed list for output)
    # result array of size N+1, index 1 to N
    result = [0] * (N + 1)

    # Process from N down to 1
    # For number i (value i), the target position in the forward process was P[i-1].
    # Let target_pos = P[i-1]. We need to find the index in the current array of empty slots
    # such that the count of empty slots up to that index is target_pos.
    
    for i in range(N, 0, -1):
        target_pos = P[i-1]
        
        # Binary lifting on BIT to find the index with cumulative sum == target_pos
        idx = 0
        current_sum = 0
        # Start from the highest power of 2 less than or equal to N
        # We can precompute or just use log2(N). 
        # Since N <= 5*10^5, 2^19 = 524288 is enough.
        bit_mask = 1 << (N.bit_length() - 1)
        
        while bit_mask > 0:
            t_idx = idx + bit_mask
            if t_idx <= N and current_sum + bit[t_idx] < target_pos:
                idx = t_idx
                current_sum += bit[idx]
            bit_mask >>= 1
        
        # The answer is idx + 1 because the loop stops when sum < target_pos
        # so the next position (idx+1) will have sum >= target_pos.
        # Since we are looking for the exact k-th empty slot, and the frequencies are 0 or 1,
        # the cumulative sum jumps by 1 at the target position.
        # So the index we want is idx + 1.
        final_idx = idx + 1
        
        # Place number i at this position
        result[final_idx] = i
        
        # Mark this position as occupied in BIT (subtract 1)
        # Update BIT: add -1 at final_idx
        k = final_idx
        while k <= N:
            bit[k] -= 1
            k += k & (-k)

    # Output the result array from index 1 to N
    print(*(result[1:]))

if __name__ == '__main__':
    solve()