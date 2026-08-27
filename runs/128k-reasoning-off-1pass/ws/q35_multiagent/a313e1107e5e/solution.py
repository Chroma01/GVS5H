import sys
from bisect import bisect_right

def solve():
    # Increase recursion depth just in case, though we use iterative BIT
    sys.setrecursionlimit(200000)
    
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
        
    # Coordinate compression for values in A
    sorted_unique_A = sorted(list(set(A)))
    val_to_rank = {val: i + 1 for i, val in enumerate(sorted_unique_A)}
    M = len(sorted_unique_A)
    
    # BIT for prefix maximums
    # tree[i] stores the max LIS length ending with a value whose rank is <= i
    # Actually, standard BIT for prefix max:
    # update(idx, val): updates position idx with val (maximize)
    # query(idx): returns max value in range [1, idx]
    
    bit = [0] * (M + 1)
    
    def bit_update(idx, val):
        """Update the BIT at index idx with value val (maximize)."""
        while idx <= M:
            if val > bit[idx]:
                bit[idx] = val
            else:
                # Since we are maximizing, if the current node is already >= val,
                # and we assume updates only increase values, we might still need to check parents?
                # No, for prefix max BIT, if bit[idx] >= val, then any parent covering idx
                # will also be >= bit[idx] >= val, so we can stop? 
                # Wait, this logic is flawed for general max BIT.
                # Standard BIT for prefix max requires that we update all covering nodes.
                # However, if we only increase values, we can just propagate.
                # But if we encounter a node that is already >= val, we don't necessarily stop
                # because a parent might be smaller? No, in a max-BIT, parent covers a range including child.
                # If child is updated to val, parent should be at least val.
                # If parent is already >= val, then it's fine.
                # So yes, we can break if bit[idx] >= val? 
                # Let's verify: bit[i] stores max of a range. If we update a point to val,
                # and the current stored max for that range is already >= val, then the max doesn't change.
                # So yes, we can break.
                pass
            idx += idx & (-idx)

    # Correct implementation for Max BIT update:
    # We must update all nodes that cover the index.
    # If bit[idx] is already >= val, we don't need to update it, but we might need to update its ancestors?
    # No, if bit[idx] >= val, then the max for the range covered by idx is already >= val.
    # The ancestors cover larger ranges that include idx. Their max is at least bit[idx] >= val.
    # So they are also >= val. So we can stop.
    def bit_update_correct(idx, val):
        while idx <= M:
            if val > bit[idx]:
                bit[idx] = val
            else:
                # Optimization: if current node is already >= val, ancestors are too.
                break
            idx += idx & (-idx)

    def bit_query(idx):
        """Query the maximum value in range [1, idx]."""
        res = 0
        while idx > 0:
            if bit[idx] > res:
                res = bit[idx]
            idx -= idx & (-idx)
        return res

    # Sort queries by R
    queries.sort(key=lambda x: x[0])
    
    answers = [0] * Q
    
    # Process array A and queries
    q_idx = 0
    num_queries = len(queries)
    
    for i in range(N):
        val = A[i]
        rank = val_to_rank[val]
        
        # Find max LIS length ending with value < val
        # We need max in ranks [1, rank-1]
        prev_max = 0
        if rank > 1:
            prev_max = bit_query(rank - 1)
            
        new_len = prev_max + 1
        
        # Update the BIT at rank with new_len
        bit_update_correct(rank, new_len)
        
        # Answer all queries with R = i + 1
        while q_idx < num_queries and queries[q_idx][0] == i + 1:
            R, X, original_idx = queries[q_idx]
            
            # Find the largest rank such that sorted_unique_A[rank-1] <= X
            # sorted_unique_A is 0-indexed. rank is 1-indexed.
            # We want largest index j in sorted_unique_A such that sorted_unique_A[j] <= X
            # bisect_right returns insertion point after all elements <= X
            # So index = bisect_right(...) - 1
            pos = bisect_right(sorted_unique_A, X)
            
            if pos == 0:
                ans = 0
            else:
                # pos is the count of elements <= X, which corresponds to rank pos
                ans = bit_query(pos)
                
            answers[original_idx] = ans
            q_idx += 1
            
    # Print answers
    for ans in answers:
        print(ans)

solve()