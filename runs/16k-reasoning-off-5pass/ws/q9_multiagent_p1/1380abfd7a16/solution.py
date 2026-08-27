import sys

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(2000)

class FenwickTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (self.n + 1)

    def update(self, i, delta):
        """Adds delta to element at index i (1-based)."""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        """Returns sum from 1 to i (1-based)."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def find_kth(self, k):
        """
        Finds the smallest index i such that query(i) >= k.
        Uses binary lifting on the Fenwick Tree for O(log n) complexity.
        Assumes the total sum is at least k.
        """
        idx = 0
        current_sum = 0
        # Determine the largest power of 2 less than or equal to n
        # We start with the highest bit.
        bit_mask = 1
        while bit_mask <= self.n:
            bit_mask <<= 1
        bit_mask >>= 1
        
        while bit_mask > 0:
            t_idx = idx + bit_mask
            if t_idx <= self.n and current_sum + self.tree[t_idx] < k:
                idx = t_idx
                current_sum += self.tree[t_idx]
            bit_mask >>= 1
        
        return idx + 1

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

    # We need to determine the final position of each number i (1 to N).
    # We work backwards from N down to 1.
    # Initially, all positions 1 to N are empty.
    # When we consider number i, it was placed at the P[i-1]-th empty position.
    # We find that position, place i there, and mark it as occupied.
    
    # Initialize Fenwick Tree with 1s for all positions 1 to N
    ft = FenwickTree(N)
    for i in range(1, N + 1):
        ft.update(i, 1)
    
    # Result array (0-indexed, but we'll fill it based on 1-based positions)
    final_array = [0] * (N + 1)
    
    # Process from N down to 1
    # P is 0-indexed in our list, so P[i-1] corresponds to the operation for number i+1
    # But the problem says: for i=1..N, insert i at P_i-th position.
    # So P[0] is for 1, P[1] is for 2, ..., P[N-1] is for N.
    
    for i in range(N, 0, -1):
        p_val = P[i-1]
        # Find the p_val-th empty position
        pos = ft.find_kth(p_val)
        final_array[pos] = i
        # Mark this position as occupied (remove 1 from count)
        ft.update(pos, -1)
    
    # Output the result from index 1 to N
    print(*(final_array[1:]))

if __name__ == '__main__':
    solve()