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

    def find_kth(self, k):
        """
        Finds the smallest index i such that the prefix sum up to i is >= k.
        Uses binary lifting on the Fenwick Tree for O(log n) complexity.
        Assumes k is valid (1 <= k <= total sum).
        Returns 1-based index.
        """
        idx = 0
        current_sum = 0
        # Determine the largest power of 2 less than or equal to n
        bit_mask = 1
        while bit_mask <= self.n:
            bit_mask <<= 1
        bit_mask >>= 1
        
        while bit_mask > 0:
            t_idx = idx + bit_mask
            if t_idx <= self.n:
                if current_sum + self.tree[t_idx] < k:
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

    # P is 1-indexed in problem description (P_i for i=1..N)
    # We store P such that P[i] corresponds to the insertion position for number i+1
    # But the problem says: for i=1..N, insert i at P_i.
    # So P[0] is position for 1, P[1] is position for 2, ..., P[N-1] is position for N.
    
    # We process backwards from N down to 1.
    # The number N is inserted at P[N-1].
    # The number i is inserted at P[i-1].
    
    # Initialize Fenwick Tree of size N
    ft = FenwickTree(N)
    
    # Initially, all positions are empty (sum = 0).
    # We want to place numbers N, N-1, ..., 1.
    # For number i (where i goes from N down to 1), we need to find the P[i-1]-th empty slot.
    # Once found, we mark that slot as occupied (add 1 to the tree).
    
    # Result array to store the final position of each number.
    # result[num] = final_index (1-based)
    result = [0] * (N + 1)
    
    # Process from N down to 1
    for i in range(N, 0, -1):
        pos = P[i-1]  # The target rank among empty slots
        final_idx = ft.find_kth(pos)
        result[i] = final_idx
        ft.update(final_idx, 1) # Mark this slot as occupied

    # Construct the final array A
    # A[final_idx - 1] = i
    final_array = [0] * N
    for i in range(1, N + 1):
        final_array[result[i] - 1] = i
        
    # Print the result
    print(*(final_array))

if __name__ == '__main__':
    solve()