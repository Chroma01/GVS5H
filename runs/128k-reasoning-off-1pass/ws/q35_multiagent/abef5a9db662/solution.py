import sys

def main():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    N = int(next(iterator))
    contests = []
    for _ in range(N):
        L = int(next(iterator))
        R = int(next(iterator))
        contests.append((L, R))
        
    Q = int(next(iterator))
    queries = []
    for _ in range(Q):
        queries.append(int(next(iterator)))
        
    MAX_X = 500000
    size = MAX_X + 1
    
    # Segment tree arrays
    # tree_min[i] stores the minimum value in the range covered by node i
    # tree_max[i] stores the maximum value in the range covered by node i
    # lazy[i] stores the pending increment for the range covered by node i
    tree_min = [0] * (4 * size)
    tree_max = [0] * (4 * size)
    lazy = [0] * (4 * size)
    
    def build(node, start, end):
        if start == end:
            tree_min[node] = start
            tree_max[node] = start
        else:
            mid = (start + end) // 2
            build(2 * node, start, mid)
            build(2 * node + 1, mid + 1, end)
            tree_min[node] = min(tree_min[2 * node], tree_min[2 * node + 1])
            tree_max[node] = max(tree_max[2 * node], tree_max[2 * node + 1])
            
    def push(node, start, end):
        if lazy[node] != 0:
            mid = (start + end) // 2
            left_node = 2 * node
            right_node = 2 * node + 1
            
            lazy[left_node] += lazy[node]
            tree_min[left_node] += lazy[node]
            tree_max[left_node] += lazy[node]
            
            lazy[right_node] += lazy[node]
            tree_min[right_node] += lazy[node]
            tree_max[right_node] += lazy[node]
            
            lazy[node] = 0
            
    def update_range(node, start, end, l, r, val):
        if r < start or end < l:
            return
        if l <= start and end <= r:
            tree_min[node] += val
            tree_max[node] += val
            lazy[node] += val
            return
        
        push(node, start, end)
        mid = (start + end) // 2
        update_range(2 * node, start, mid, l, r, val)
        update_range(2 * node + 1, mid + 1, end, l, r, val)
        tree_min[node] = min(tree_min[2 * node], tree_min[2 * node + 1])
        tree_max[node] = max(tree_max[2 * node], tree_max[2 * node + 1])
        
    def find_first_ge(node, start, end, val):
        """Find the smallest index in [start, end] with value >= val."""
        if tree_min[node] >= val:
            if start == end:
                return start
            push(node, start, end)
            mid = (start + end) // 2
            if tree_min[2 * node] >= val:
                return find_first_ge(2 * node, start, mid, val)
            else:
                return find_first_ge(2 * node + 1, mid + 1, end, val)
        else:
            # If the min in this node is less than val, we need to search deeper
            if start == end:
                return -1 # Should not happen if called correctly
            
            push(node, start, end)
            mid = (start + end) // 2
            # Try left child first
            res = find_first_ge(2 * node, start, mid, val)
            if res != -1:
                return res
            return find_first_ge(2 * node + 1, mid + 1, end, val)

    def find_last_le(node, start, end, val):
        """Find the largest index in [start, end] with value <= val."""
        if tree_max[node] <= val:
            if start == end:
                return start
            push(node, start, end)
            mid = (start + end) // 2
            if tree_max[2 * node + 1] <= val:
                return find_last_le(2 * node + 1, mid + 1, end, val)
            else:
                return find_last_le(2 * node, start, mid, val)
        else:
            if start == end:
                return -1
            
            push(node, start, end)
            mid = (start + end) // 2
            # Try right child first
            res = find_last_le(2 * node + 1, mid + 1, end, val)
            if res != -1:
                return res
            return find_last_le(2 * node, start, mid, val)

    build(1, 1, MAX_X)
    
    for L, R in contests:
        # Find the first index where current rating >= L
        l_idx = find_first_ge(1, 1, MAX_X, L)
        
        # Find the last index where current rating <= R
        r_idx = find_last_le(1, 1, MAX_X, R)
        
        if l_idx != -1 and r_idx != -1 and l_idx <= r_idx:
            update_range(1, 1, MAX_X, l_idx, r_idx, 1)
            
    results = []
    for x in queries:
        # Query the final rating for initial rating x
        # We can do a point query by traversing down or just use a helper
        # Since we only need point queries at the end, we can implement a point query
        # Or we can just traverse the tree. Let's implement a simple point query.
        
        # To get the value at index x, we can use a function that pushes all lazy values down to the leaf
        def query_point(node, start, end, idx):
            if start == end:
                return tree_min[node]
            push(node, start, end)
            mid = (start + end) // 1
            mid = (start + end) // 2
            if idx <= mid:
                return query_point(2 * node, start, mid, idx)
            else:
                return query_point(2 * node + 1, mid + 1, end, idx)
                
        results.append(str(query_point(1, 1, MAX_X, x)))
        
    print('\n'.join(results))

if __name__ == '__main__':
    main()