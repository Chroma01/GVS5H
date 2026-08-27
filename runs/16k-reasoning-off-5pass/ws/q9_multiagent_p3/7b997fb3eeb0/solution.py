import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            l = int(next(iterator))
            r = int(next(iterator))
            queries.append((l, r))
    except StopIteration:
        return

    # Segment Tree Implementation
    # Size needs to be power of 2 for simplicity in iterative implementation
    size = 1
    while size < N:
        size *= 2
    
    # Tree array: each node stores (pairs_count, next_start_index, end_index)
    # next_start_index: index of the first element NOT used as a top (smallest available)
    # end_index: index of the largest element available as a base (largest available)
    # If a node is empty (out of bounds), we use a sentinel.
    INF = N + 100
    EMPTY = (0, INF, INF)
    
    tree = [EMPTY] * (2 * size)
    
    # Initialize leaves
    for i in range(N):
        tree[size + i] = (0, i, i)
    
    # Merge Logic
    def merge_nodes(left, right, A):
        # left = (pairs_l, start_l, end_l)
        # right = (pairs_r, start_r, end_r)
        
        # Check for empty nodes
        if left[1] == INF:
            return right
        if right[1] == INF:
            return left
            
        pairs_l, start_l, end_l = left
        pairs_r, start_r, end_r = right
        
        # We need to match tops from [start_l, end_l] with bases from [start_r, end_r]
        # Tops are A[start_l], A[start_l+1]...
        # Bases are A[end_r], A[end_r-1]...
        # We want max k such that A[start_l + i] * 2 <= A[end_r - i] for all 0 <= i < k
        
        len_tops = end_l - start_l + 1
        len_bases = end_r - start_r + 1
        limit = min(len_tops, len_bases)
        
        low = 0
        high = limit
        ans_k = 0
        
        # Binary search for k
        while low <= high:
            mid_k = (low + high) // 2
            if mid_k == 0:
                ans_k = max(ans_k, mid_k)
                low = mid_k + 1
                continue
            
            # Check the tightest constraint (last pair)
            # Top index: start_l + mid_k - 1
            # Base index: end_r - (mid_k - 1)
            top_idx = start_l + mid_k - 1
            base_idx = end_r - mid_k + 1
            
            if A[top_idx] * 2 <= A[base_idx]:
                ans_k = mid_k
                low = mid_k + 1
            else:
                high = mid_k - 1
        
        extra_pairs = ans_k
        new_pairs = pairs_l + pairs_r + extra_pairs
        new_start = start_l + extra_pairs
        # The bases used are the largest 'extra_pairs' from the right range.
        # The remaining bases are from start_r to end_r - extra_pairs.
        new_end = end_r - extra_pairs
        
        return (new_pairs, new_start, new_end)

    # Build the tree
    for i in range(size - 1, 0, -1):
        tree[i] = merge_nodes(tree[2 * i], tree[2 * i + 1], A)

    # Query function
    def query(l, r):
        # Range [l, r] inclusive (0-based)
        L_idx = size + l
        R_idx = size + r
        
        nodes = []
        
        while L_idx <= R_idx:
            if L_idx % 2 == 1:
                nodes.append(tree[L_idx])
                L_idx += 1
            if R_idx % 2 == 0:
                nodes.append(tree[R_idx])
                R_idx -= 1
            L_idx //= 2
            R_idx //= 2
        
        # Sort nodes by start index to ensure correct merge order (smallest to largest)
        nodes.sort(key=lambda x: x[1])
        
        if not nodes:
            return (0, INF, INF)
            
        res = nodes[0]
        for i in range(1, len(nodes)):
            res = merge_nodes(res, nodes[i], A)
            
        return res

    results = []
    for l, r in queries:
        # Convert 1-based to 0-based
        l0 = l - 1
        r0 = r - 1
        res = query(l0, r0)
        results.append(str(res[0]))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()