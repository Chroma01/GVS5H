import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    P = []
    for i in range(N):
        P.append(int(data[i+1]))
    
    # BIT (Fenwick Tree) to manage available positions
    # bit[i] stores the sum of frequencies from index 1 to i
    # Initially all positions 1..N are available (value 1)
    bit = [0] * (N + 1)
    
    def update(idx, val):
        """Add val to element at idx (1-based)"""
        while idx <= N:
            bit[idx] += val
            idx += idx & (-idx)
            
    def query(idx):
        """Return sum from 1 to idx"""
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s
    
    # Initialize BIT with 1s at all positions
    # We can do this efficiently by setting bit[i] = lowbit(i) initially
    # since each position has value 1, the prefix sum up to i is i.
    # But let's just build it properly or use the property:
    # For an array of all 1s, bit[i] = lowbit(i)
    for i in range(1, N + 1):
        bit[i] = i & (-i)
        
    # Function to find the k-th available position using binary lifting on BIT
    def find_kth(k):
        """Find the smallest index idx such that query(idx) == k"""
        idx = 0
        current_sum = 0
        # Find the largest power of 2 less than or equal to N
        bit_mask = 1
        while bit_mask <= N:
            bit_mask <<= 1
        bit_mask >>= 1
        
        while bit_mask > 0:
            t_idx = idx + bit_mask
            if t_idx <= N and current_sum + bit[t_idx] < k:
                idx = t_idx
                current_sum += bit[t_idx]
            bit_mask >>= 1
            
        return idx + 1
    
    # Array to store the final result
    ans = [0] * (N + 1)
    
    # Process from N down to 1
    # P is 0-indexed in our list, so P[i-1] corresponds to P_i
    for i in range(N, 0, -1):
        p_i = P[i-1]
        # Find the p_i-th available position
        pos = find_kth(p_i)
        # Place number i at this position
        ans[pos] = i
        # Mark this position as occupied (subtract 1)
        update(pos, -1)
        
    # Output the result
    print(' '.join(map(str, ans[1:])))

if __name__ == '__main__':
    solve()