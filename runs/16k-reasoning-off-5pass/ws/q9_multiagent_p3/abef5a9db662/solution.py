import sys

# Increase recursion depth to handle deep recursion in Segment Tree operations
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        L = []
        R = []
        for _ in range(N):
            L.append(int(next(iterator)))
            R.append(int(next(iterator)))
        
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            queries.append(int(next(iterator)))
    except StopIteration:
        return

    # Maximum possible rating
    # Max initial X is 500,000. Max increase is N (200,000).
    # So max rating is around 700,000.
    MAX_VAL = 500000 + N + 5
    
    # Segment Tree Arrays
    # We use 1-based indexing for nodes.
    # tree_size needs to be sufficient for range [1, MAX_VAL]
    size = MAX_VAL
    tree_size = 4 * size
    
    min_val = [0] * tree_size
    max_val = [0] * tree_size
    lazy = [0] * tree_size
    
    # Build the tree
    # Initially, rating[x] = x.
    # min_val[node] stores the value of the leftmost element in the range covered by node.
    # max_val[node] stores the value of the rightmost element in the range covered by node.
    # Since the array is sorted, min is at left, max is at right.
    
    def build(node, start, end):
        if start == end:
            min_val[node] = start
            max_val[node] = start
        else:
            mid = (start + end) // 2
            build(2 * node, start, mid)
            build(2 * node + 1, mid + 1, end)
            min_val[node] = min_val[2 * node]
            max_val[node] = max_val[2 * node + 1]
            
    build(1, 1, size)
    
    def push(node):
        if lazy[node] != 0:
            left = 2 * node
            right = 2 * node + 1
            
            lazy[left] += lazy[node]
            min_val[left] += lazy[node]
            max_val[left] += lazy[node]
            
            lazy[right] += lazy[node]
            min_val[right] += lazy[node]
            max_val[right] += lazy[node]
            
            lazy[node] = 0

    def update(node, start, end, l, r, val):
        if l > end or r < start:
            return
        if l <= start and end <= r:
            lazy[node] += val
            min_val[node] += val
            max_val[node] += val
            return
        
        push(node)
        mid = (start + end) // 2
        update(2 * node, start, mid, l, r, val)
        update(2 * node + 1, mid + 1, end, l, r, val)
        
        min_val[node] = min(min_val[2 * node], min_val[2 * node + 1])
        max_val[node] = max(max_val[2 * node], max_val[2 * node + 1])

    # Find first index >= X
    def find_first_ge(node, start, end, X):
        # If the minimum value in this range is >= X, then the first element >= X 
        # is the leftmost element of this range (because the array is sorted).
        if min_val[node] >= X:
            return start
        
        # If the maximum value in this range is < X, then no element in this range is >= X.
        if max_val[node] < X:
            return -1
            
        push(node)
        mid = (start + end) // 2
        
        res = find_first_ge(2 * node, start, mid, X)
        if res != -1:
            return res
        return find_first_ge(2 * node + 1, mid + 1, end, X)

    # Find last index <= X
    def find_last_le(node, start, end, X):
        # If the maximum value in this range is <= X, then the last element <= X 
        # is the rightmost element of this range.
        if max_val[node] <= X:
            return end
        
        # If the minimum value in this range is > X, then no element in this range is <= X.
        if min_val[node] > X:
            return -1
            
        push(node)
        mid = (start + end) // 2
        
        res = find_last_le(2 * node + 1, mid + 1, end, X)
        if res != -1:
            return res
        return find_last_le(2 * node, start, mid, X)

    # Process contests
    for i in range(N):
        l_contest = L[i]
        r_contest = R[i]
        
        # Find range of starting indices [start_idx, end_idx]
        # such that current_rating[start_idx] >= l_contest
        # and current_rating[end_idx] <= r_contest
        
        start_idx = find_first_ge(1, 1, size, l_contest)
        end_idx = find_last_le(1, 1, size, r_contest)
        
        if start_idx != -1 and end_idx != -1 and start_idx <= end_idx:
            update(1, 1, size, start_idx, end_idx, 1)
            
    # Answer queries
    results = []
    for x in queries:
        # Point query: get value at index x
        node = 1
        start = 1
        end = size
        while start != end:
            push(node)
            mid = (start + end) // 2
            if x <= mid:
                node = 2 * node
                end = mid
            else:
                node = 2 * node + 1
                start = mid + 1
        
        # Leaf node
        results.append(min_val[node])
        
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()