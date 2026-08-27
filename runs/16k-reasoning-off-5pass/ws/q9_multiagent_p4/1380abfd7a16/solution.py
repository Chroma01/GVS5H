import sys

# Increase recursion depth just in case, though we use iterative approach
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
        Finds the smallest index i such that sum(1..i) >= k.
        Uses binary lifting on the Fenwick Tree for O(log n) complexity.
        Assumes k is valid (1 <= k <= total sum).
        """
        idx = 0
        current_sum = 0
        # Determine the highest power of 2 less than or equal to n
        # We can start from the largest power of 2 <= n
        bit_mask = 1
        while bit_mask <= self.n:
            bit_mask <<= 1
        bit_mask >>= 1

        while bit_mask > 0:
            t_idx = idx + bit_mask
            if t_idx <= self.n and current_sum + self.tree[t_idx] < k:
                idx = t_idx
                current_sum += self.tree[idx]
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

    # P is 0-indexed in our list, but problem uses 1-based indexing for P_i
    # P[i] corresponds to the insertion position for number (i+1)
    # We need to process from N down to 1.
    # The value at index i in P corresponds to number (i+1)
    # So P[N-1] is the position for number N.
    
    # We will store the final position for each number 1..N
    # result[i] will store the final position (1-based) of number i
    result = [0] * (N + 1)
    
    # Initialize Fenwick Tree of size N
    ft = FenwickTree(N)
    
    # Process backwards from N to 1
    # For number i (where i goes from N down to 1):
    # The target position is P[i-1] (since P is 0-indexed list)
    # We need to find the P[i-1]-th empty slot.
    
    for i in range(N, 0, -1):
        target_pos = P[i-1]
        # Find the actual index in the final array
        final_idx = ft.find_kth(target_pos)
        result[i] = final_idx
        # Mark this position as occupied
        ft.update(final_idx, 1)
    
    # Construct the final array
    # We have positions for each number. We need to place them.
    # Create an array of size N (0-indexed for output)
    final_array = [0] * N
    for num in range(1, N + 1):
        pos = result[num] - 1 # Convert to 0-based index
        final_array[pos] = num
        
    # Print the result
    print(*(final_array))

if __name__ == '__main__':
    solve()