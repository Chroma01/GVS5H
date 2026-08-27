import sys

# Increase recursion depth just in case, though we will use iterative BIT
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
    # 1-indexed internally
    class FenwickTree:
        def __init__(self, size):
            self.n = size
            self.tree = [0] * (self.n + 1)

        def update(self, i, delta):
            """Adds delta to element at index i (1-based)"""
            while i <= self.n:
                self.tree[i] += delta
                i += i & (-i)

        def query(self, i):
            """Returns sum of elements from 1 to i (1-based)"""
            s = 0
            while i > 0:
                s += self.tree[i]
                i -= i & (-i)
            return s

    # We need to count for each P[i], how many elements to its left are greater than P[i].
    # We can do this by iterating from left to right.
    # For current element x = P[i], the number of elements greater than x already seen is:
    # (total elements seen so far) - (number of elements <= x seen so far).
    # Since we are processing a permutation of 1..N, "elements <= x seen so far" is query(x).
    # "Total elements seen so far" is i (0-indexed count, so i elements before current).
    
    # Initialize Fenwick Tree with size N
    bit = FenwickTree(N)
    
    total_cost = 0
    
    for i in range(N):
        x = P[i]
        
        # Number of elements seen so far is i (since we are at index i, 0-based)
        # Number of elements <= x seen so far is bit.query(x)
        # Number of elements > x seen so far is i - bit.query(x)
        
        count_greater = i - bit.query(x)
        
        # Add contribution to total cost
        total_cost += x * count_greater
        
        # Add current element x to the BIT
        bit.update(x, 1)
        
    print(total_cost)

if __name__ == '__main__':
    solve()