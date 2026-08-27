import sys

# Increase recursion depth just in case, though iterative segment tree is preferred
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
        
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            l = int(next(iterator))
            r = int(next(iterator))
            queries.append((l, r))
    except StopIteration:
        return

    # Segment Tree Implementation
    # Each node stores a list of survivors (sorted ascending for storage)
    # Since the array A is sorted, the left child's range has smaller values than the right child's.
    
    # We will use an iterative segment tree.
    # Tree size: 2^ceil(log2(N)) * 2
    size = 1
    while size < N:
        size *= 2
    
    # tree[i] will store the list of survivors for the range covered by node i
    tree = [[] for _ in range(2 * size)]
    
    # Initialize leaves
    for i in range(N):
        tree[size + i] = [A[i]]
    
    # Merge function logic:
    # Given left_list (L) and right_list (R)
    # All elements in R are > all elements in L (because A is sorted)
    # We process R (largest first) and try to match with L (largest available <= r/2)
    
    def merge_lists(left_list, right_list):
        # Optimization: If one list is empty, return the other
        if not left_list:
            return right_list
        if not right_list:
            return left_list
            
        # Convert to descending for processing (largest first)
        l_desc = left_list[::-1]
        r_desc = right_list[::-1]
        
        new_left = []
        new_right = []
        
        # Pointer for l_desc (starting from largest)
        ptr = 0
        len_l = len(l_desc)
        
        for r in r_desc:
            # Find largest l such that l <= r/2
            # Since l_desc is descending, we want the first element that is <= r/2.
            # All elements before that are > r/2.
            while ptr < len_l and l_desc[ptr] > r / 2:
                ptr += 1
            
            if ptr < len_l:
                # Match found: l_desc[ptr] and r
                # Both are used.
                ptr += 1
                # r is used, so not added to new_right
            else:
                # No match for r
                new_right.append(r)
        
        # Remaining elements in l_desc (from ptr onwards) are unmatched
        # They go to new_left. l_desc is descending, so we reverse to make ascending.
        remaining_l = l_desc[ptr:]
        remaining_l.reverse()
        
        # new_right was collected in descending order. Reverse to make ascending.
        new_right.reverse()
        
        return remaining_l + new_right

    # Build the tree
    for i in range(size - 1, 0, -1):
        tree[i] = merge_lists(tree[2 * i], tree[2 * i + 1])

    # Query function to return the count of pairs
    def query_count(l, r):
        # l, r are 0-based indices
        left_nodes = []
        right_nodes = []
        
        l += size
        r += size
        
        while l <= r:
            if l % 2 == 1:
                left_nodes.append(tree[l])
                l += 1
            if r % 2 == 0:
                right_nodes.append(tree[r])
                r -= 1
            l //= 2
            r //= 2
        
        # right_nodes are collected from right to left, reverse to get left-to-right order
        right_nodes.reverse()
        
        current_list = []
        pairs_count = 0
        
        for node in left_nodes + right_nodes:
            # Merge current_list with node
            old_len = len(current_list)
            new_list = merge_lists(current_list, node)
            new_len = len(new_list)
            
            # Elements removed = old_len + len(node) - new_len
            # Each pair removes 2 elements
            pairs_count += (old_len + len(node) - new_len) // 2
            
            current_list = new_list
            
        return pairs_count

    results = []
    for l, r in queries:
        # Input L, R are 1-based inclusive. Convert to 0-based.
        ans = query_count(l - 1, r - 1)
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()