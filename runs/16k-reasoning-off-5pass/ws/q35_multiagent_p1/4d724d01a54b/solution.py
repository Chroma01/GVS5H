import sys

# Increase recursion depth just in case, though we won't use recursion
sys.setrecursionlimit(200005)

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

    # We need to calculate sum_{i=1}^{N-1} i * C_i
    # where C_i is the number of elements in P[0...i-1] (1-based index 1 to i)
    # that are greater than i.
    
    # C_i = i - (number of elements in P[0...i-1] that are <= i)
    
    # We can use a Fenwick Tree (Binary Indexed Tree) to count elements <= i
    # efficiently as we iterate.
    
    # Fenwick Tree implementation
    # 1-indexed BIT
    bit = [0] * (N + 1)
    
    def update(idx, val):
        """Add val to element at idx (1-based)"""
        while idx <= N:
            bit[idx] += val
            idx += idx & (-idx)
            
    def query(idx):
        """Return sum from 1 to idx (1-based)"""
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & (-idx)
        return s

    total_cost = 0
    
    # Iterate i from 1 to N-1 (1-based index for the boundary)
    # At step i, we have processed P[0]...P[i-1] (which are the first i elements)
    # We add P[i-1] to the BIT, then query how many are <= i.
    
    for i in range(1, N):
        # The element at 0-based index i-1 is the i-th element
        val = P[i-1]
        
        # Add this value to the BIT
        update(val, 1)
        
        # Count how many elements in the current prefix (first i elements) are <= i
        count_le_i = query(i)
        
        # C_i = i - count_le_i
        C_i = i - count_le_i
        
        # Add cost: i * C_i
        total_cost += i * C_i
        
    print(total_cost)

if __name__ == '__main__':
    solve()