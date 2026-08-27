import sys

# Increase recursion depth to handle deep segment trees if necessary
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        # 1-based indexing for A to match problem statement and query logic easily
        A = [0] * (N + 1)
        for i in range(1, N + 1):
            A[i] = int(next(iterator))
        
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            l = int(next(iterator))
            r = int(next(iterator))
            queries.append((l, r))
    except StopIteration:
        return

    # Segment Tree Implementation
    # Tree size: 4 * N
    tree_size = 4 * N
    # pairs[i] stores max pairs in range covered by node i
    # unused[i] stores count of unused elements (which are the smallest ones) in range covered by node i
    pairs = [0] * tree_size
    unused = [0] * tree_size
    
    # Helper to merge two nodes
    # left_rem: number of unused elements in the left part (smallest ones)
    # right_rem: number of unused elements in the right part (smallest ones)
    # We want to match the largest available from Right (bottoms) with the largest available from Left (tops).
    # Largest available in Left is at index: left_start + left_rem - 1
    # Largest available in Right is at index: right_start + right_rem - 1
    def merge_nodes(left_start, left_end, right_start, right_end, left_rem, right_rem):
        if left_rem == 0 or right_rem == 0:
            return 0, 0 
        
        # We binary search for the number of pairs k.
        # The condition is: for the k-th pair (counting from largest available),
        # A[left_start + left_rem - k] <= A[right_start + right_rem - k] // 2
        # Due to the sorted nature, if this holds for k, it implies it holds for all j < k 
        # (because the values decrease as k increases, but the gap logic in this specific problem 
        # allows binary search on the boundary condition).
        
        low = 0
        high = min(left_rem, right_rem)
        ans_k = 0
        
        while low <= high:
            mid_k = (low + high) // 2
            if mid_k == 0:
                ans_k = max(ans_k, mid_k)
                low = mid_k + 1
                continue
            
            idx_l = left_start + left_rem - mid_k
            idx_r = right_start + right_rem - mid_k
            
            if A[idx_l] <= A[idx_r] // 2:
                ans_k = mid_k
                low = mid_k + 1
            else:
                high = mid_k - 1
        
        return ans_k, ans_k 

    # Build the tree
    def build(node, start, end):
        if start == end:
            pairs[node] = 0
            unused[node] = 1
            return
        mid = (start + end) // 2
        left_child = 2 * node
        right_child = 2 * node + 1
        build(left_child, start, mid)
        build(right_child, mid + 1, end)
        
        added_pairs, added_unused = merge_nodes(start, mid, mid + 1, end, unused[left_child], unused[right_child])
        
        pairs[node] = pairs[left_child] + pairs[right_child] + added_pairs
        unused[node] = unused[left_child] + unused[right_child] - 2 * added_unused

    # Query function
    # Returns (cnt, unused, start_index, length)
    def query_range(node, start, end, l, r):
        if r < start or end < l:
            return None
        if l <= start and end <= r:
            return (pairs[node], unused[node], start, end - start + 1)
        mid = (start + end) // 2
        left_res = query_range(2 * node, start, mid, l, r)
        right_res = query_range(2 * node + 1, mid + 1, end, l, r)
        
        if left_res is None:
            return right_res
        if right_res is None:
            return left_res
        
        cnt_l, rem_l, s_l, len_l = left_res
        cnt_r, rem_r, s_r, len_r = right_res
        
        added_pairs, added_unused = merge_nodes(s_l, s_l + len_l - 1, s_r, s_r + len_r - 1, rem_l, rem_r)
        
        new_cnt = cnt_l + cnt_r + added_pairs
        new_rem = rem_l + rem_r - 2 * added_unused
        
        return (new_cnt, new_rem, s_l, len_l + len_r)

    build(1, 1, N)
    
    results = []
    for l, r in queries:
        res = query_range(1, 1, N, l, r)
        if res is None:
            results.append(0)
        else:
            results.append(res[0])
            
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()