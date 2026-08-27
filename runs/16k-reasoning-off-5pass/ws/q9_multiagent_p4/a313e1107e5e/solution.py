import sys
from bisect import bisect_right

# Increase recursion depth just in case, though we use iterative BIT
sys.setrecursionlimit(200005)

def solve():
    # Fast I/O
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    A = []
    for _ in range(N):
        A.append(int(next(iterator)))
    
    queries = []
    for i in range(Q):
        R = int(next(iterator))
        X = int(next(iterator))
        queries.append((R, X, i))
    
    # Coordinate Compression
    # We need to map values in A to ranks [1, num_unique]
    # For X values, we need to find the rank corresponding to "count of elements <= X"
    # which is exactly bisect_right on the sorted unique values.
    
    sorted_unique_A = sorted(list(set(A)))
    rank_map = {val: i + 1 for i, val in enumerate(sorted_unique_A)}
    num_unique = len(sorted_unique_A)
    
    # Prepare queries for offline processing
    # Sort queries by R (prefix length)
    queries.sort(key=lambda x: x[0])
    
    # Fenwick Tree (Binary Indexed Tree) for Range Maximum Query
    # bit[i] stores the max LIS length ending with a value having rank i
    bit = [0] * (num_unique + 1)
    
    def update(idx, val):
        """Update the BIT at idx with val (maximize)."""
        while idx <= num_unique:
            if val > bit[idx]:
                bit[idx] = val
            idx += idx & (-idx)
            
    def query(idx):
        """Query the maximum value in range [1, idx]."""
        res = 0
        while idx > 0:
            if bit[idx] > res:
                res = bit[idx]
            idx -= idx & (-idx)
        return res
    
    answers = [0] * Q
    current_idx = 0
    
    # Iterate through the array A and process queries
    for i in range(N):
        val = A[i]
        rank_val = rank_map[val]
        
        # Calculate LIS length ending at current value
        # We need strictly increasing, so we query for values strictly less than val
        # which corresponds to rank < rank_val.
        # Since ranks are 1-based and unique, rank_val-1 covers all strictly smaller ranks.
        current_len = query(rank_val - 1) + 1
        
        # Update the BIT
        update(rank_val, current_len)
        
        # Process all queries that end at this prefix (R = i + 1)
        while current_idx < Q and queries[current_idx][0] == i + 1:
            R, X, original_idx = queries[current_idx]
            
            # Find the rank for X. 
            # We want the max LIS using elements <= X.
            # In our coordinate compressed system, this means querying the BIT 
            # up to the index that represents the count of unique elements <= X.
            # bisect_right gives the insertion point after all elements <= X.
            # Since ranks are 1-based indices of sorted_unique_A, 
            # the number of elements <= X is exactly the index returned by bisect_right.
            # If bisect_right returns k, it means there are k elements <= X in sorted_unique_A.
            # These elements have ranks 1 to k. So we query BIT at k.
            
            x_rank = bisect_right(sorted_unique_A, X)
            
            # If X is smaller than the minimum element in A, x_rank will be 0.
            # The problem guarantees X >= min(A[1..R]), so x_rank >= 1.
            # However, if x_rank is 0 (hypothetically), query(0) returns 0, which is correct.
            
            ans = query(x_rank)
            answers[original_idx] = ans
            
            current_idx += 1
            
    # Print answers in original order
    print('\n'.join(map(str, answers)))

if __name__ == '__main__':
    solve()