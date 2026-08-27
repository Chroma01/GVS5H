import sys

# Increase recursion depth just in case, though we use iterative BIT
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

    # If N is 1, cost is 0
    if N <= 1:
        print(0)
        return

    # We need to calculate the minimum cost to sort the permutation.
    # The cost of swapping adjacent elements at indices i and i+1 (1-based) is i.
    # In 0-based indexing, swapping indices j and j+1 costs j+1.
    #
    # The key insight is that the minimum cost is the sum over all boundaries j (0 to N-2)
    # of (cost of boundary j) * (number of swaps across boundary j).
    # The number of swaps across boundary j (between index j and j+1) is equal to
    # the number of elements that start in the left part (indices 0..j) but belong
    # in the right part (indices j+1..N-1).
    #
    # An element with value v belongs at index v-1 (0-based).
    # So, for a boundary j, an element P[k] (where k <= j) contributes to the swap count
    # if its target position (P[k]-1) is > j.
    # i.e., P[k] - 1 > j  =>  P[k] > j + 1.
    #
    # Let C_j be the count of k in 0..j such that P[k] > j+1.
    # Then the cost contribution for boundary j is (j+1) * C_j.
    #
    # We can compute C_j efficiently using a Fenwick Tree (BIT).
    # C_j = (Total elements in 0..j) - (Count of elements in 0..j that are <= j+1)
    # C_j = (j+1) - query_BIT(j+1)
    #
    # We iterate j from 0 to N-2.
    # At each step j, we add P[j] to the BIT, then query the count of numbers <= j+1.

    # BIT implementation
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
    
    # We process boundaries j from 0 to N-2.
    # For boundary j, we consider elements P[0]...P[j].
    # So we need to have added P[0]...P[j] to the BIT before querying for boundary j.
    
    for j in range(N - 1):
        # Add P[j] to BIT. P[j] is 1-based value.
        val = P[j]
        update(val, 1)
        
        # Calculate C_j
        # Count of elements in P[0..j] that are <= j+1
        count_le = query(j + 1)
        
        # Total elements in P[0..j] is j+1
        # C_j = (j+1) - count_le
        c_j = (j + 1) - count_le
        
        # Cost for this boundary is (j+1) * c_j
        total_cost += (j + 1) * c_j

    print(total_cost)

if __name__ == '__main__':
    solve()