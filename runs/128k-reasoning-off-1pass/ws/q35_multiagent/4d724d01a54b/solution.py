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

    # Fenwick Tree (Binary Indexed Tree) implementation
    # 1-indexed
    class FenwickTree:
        def __init__(self, size):
            self.n = size
            self.tree = [0] * (self.n + 1)
        
        def update(self, i, delta):
            """Add delta to element at index i (1-based)"""
            while i <= self.n:
                self.tree[i] += delta
                i += i & (-i)
        
        def query(self, i):
            """Return prefix sum up to index i (1-based)"""
            s = 0
            while i > 0:
                s += self.tree[i]
                i -= i & (-i)
            return s

    # Initialize Fenwick Tree with size N
    ft = FenwickTree(N)
    
    total_cost = 0
    
    # Iterate through the array. We consider boundaries i from 1 to N-1.
    # At step i (1-based index in the loop, corresponding to processing P[i-1]),
    # we have processed the prefix P[0...i-1] (which has length i).
    # We want to calculate L_i = number of elements in P[0...i-1] that are > i.
    # L_i = i - (number of elements in P[0...i-1] that are <= i).
    
    for i in range(1, N):
        # The current element to add to the BIT is P[i-1]
        val = P[i-1]
        
        # Update the BIT with the current value
        ft.update(val, 1)
        
        # Count how many elements in the current prefix (of length i) are <= i
        # This is simply the prefix sum of the BIT up to index i
        count_le_i = ft.query(i)
        
        # L_i is the number of elements in the prefix that are > i
        L_i = i - count_le_i
        
        # Add the cost contribution: i * L_i
        total_cost += i * L_i
        
    print(total_cost)

if __name__ == '__main__':
    solve()