import sys
import bisect

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
        queries = []
        for i in range(Q):
            R = int(next(iterator))
            X = int(next(iterator))
            queries.append((R, X, i))
            
    except StopIteration:
        return

    # Coordinate Compression for A values
    # We map the unique values present in A to ranks 1..M.
    # This allows us to use a Fenwick Tree (BIT) of size M.
    sorted_unique_A = sorted(list(set(A)))
    rank_map = {val: i + 1 for i, val in enumerate(sorted_unique_A)}
    M = len(sorted_unique_A)
    
    # Prepare queries for offline processing
    # Sort queries by R (prefix length) to process them as we iterate through A
    queries.sort(key=lambda x: x[0])
    
    # Fenwick Tree (Binary Indexed Tree) for Range Maximum Query
    # Supports: update(index, value) -> tree[index] = max(tree[index], value)
    #          query(index) -> max(tree[1]...tree[index])
    bit = [0] * (M + 1)
    
    def update(idx, val):
        """Updates the BIT at idx with val, maintaining the maximum."""
        while idx <= M:
            if val > bit[idx]:
                bit[idx] = val
            idx += idx & (-idx)
            
    def query(idx):
        """Returns the maximum value in the range [1, idx]."""
        res = 0
        while idx > 0:
            if bit[idx] > res:
                res = bit[idx]
            idx -= idx & (-idx)
        return res

    results = [0] * Q
    
    current_q_idx = 0
    num_queries = len(queries)
    
    # Process elements of A one by one (from index 1 to N)
    for r in range(1, N + 1):
        val = A[r-1]
        rank = rank_map[val]
        
        # Find LIS length ending with a value strictly less than val.
        # Since we want strictly increasing, we query for max length ending at any value with rank < rank.
        prev_len = query(rank - 1)
        new_len = prev_len + 1
        
        # Update the BIT at position 'rank' with new_len.
        # We use max because multiple occurrences of 'val' might appear, 
        # and we want the longest chain ending with 'val' seen so far.
        update(rank, new_len)
        
        # Answer all queries that end at current_r (prefix length r)
        while current_q_idx < num_queries and queries[current_q_idx][0] == r:
            _, X, original_idx = queries[current_q_idx]
            
            # Find the rank of the largest value in A that is <= X.
            # We use bisect_right on sorted_unique_A.
            # bisect_right returns the insertion point after elements <= X.
            # So elements at indices 0 to idx_in_sorted-1 are <= X.
            # The ranks are 1-based, so the max rank is idx_in_sorted.
            idx_in_sorted = bisect.bisect_right(sorted_unique_A, X)
            max_rank = idx_in_sorted
            
            # If max_rank is 0, it means no element in A is <= X.
            # However, the problem guarantees X >= min(A[1..R]), so max_rank >= 1.
            ans = query(max_rank)
            results[original_idx] = ans
            
            current_q_idx += 1
            
    # Print results in original order
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()