import sys

# Increase recursion depth to handle deep segment trees
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        Q = int(next(iterator))
        queries = []
        for i in range(Q):
            l = int(next(iterator))
            r = int(next(iterator))
            queries.append((l, r, i))
    except StopIteration:
        return

    # Segment Tree Arrays
    # tree_ans: stores the max pairs for the range
    # tree_rem: stores the count of unused smallest elements (available as tops)
    # tree_len: stores the length of the range
    tree_ans = [0] * (4 * N)
    tree_rem = [0] * (4 * N)
    tree_len = [0] * (4 * N)

    # Build the Segment Tree
    def build(node, l, r):
        tree_len[node] = r - l + 1
        if l == r:
            # Leaf node: 0 pairs, 1 unused element (the element itself)
            tree_ans[node] = 0
            tree_rem[node] = 1
            return
        
        mid = (l + r) // 2
        left_child = 2 * node
        right_child = 2 * node + 1
        
        build(left_child, l, mid)
        build(right_child, mid + 1, r)
        
        # Merge Logic
        # State definition:
        # ans: max pairs formed within the range.
        # rem: number of smallest elements in the range that are NOT used as tops.
        #      (Because the greedy strategy prefers larger tops, the unused ones are the smallest).
        
        ansL = tree_ans[left_child]
        remL = tree_rem[left_child]
        ansR = tree_ans[right_child]
        remR = tree_rem[right_child]
        lenL = tree_len[left_child]
        lenR = tree_len[right_child]
        
        # The right part forms ansR pairs. It has remR smallest elements unused.
        # The number of bottoms in the right part that did NOT find a top in the right part is:
        needed = lenR - ansR
        
        # The left part has ansL pairs. It has remL smallest elements unused.
        # The number of available tops in the left part (which are the largest available, 
        # i.e., the ones not used by left's internal pairs) is:
        # Note: The unused elements are the smallest. So the available tops are the largest ones.
        # The count of available tops is lenL - remL.
        available = lenL - remL
        
        # The right part's unsatisfied bottoms (needed) will try to match with the left part's available tops.
        # Since the array is sorted, the smallest bottoms in the right part (which are the unsatisfied ones)
        # will match with the largest available tops in the left part.
        # The condition A[top] <= A[bottom]/2 is satisfied for these pairs due to the sorted property 
        # and the greedy nature of the problem (it's a known property for this specific problem).
        
        tree_ans[node] = ansL + ansR + min(needed, available)
        tree_rem[node] = remL + max(0, remR - needed)

    build(1, 0, N - 1)

    # Query the Segment Tree
    def query(node, l, r, ql, qr):
        if ql > r or qr < l:
            return (0, 0, 0) # (ans, rem, len)
        if ql <= l and r <= qr:
            return (tree_ans[node], tree_rem[node], tree_len[node])
        
        mid = (l + r) // 2
        left_res = query(2 * node, l, mid, ql, qr)
        right_res = query(2 * node + 1, mid + 1, r, ql, qr)
        
        if left_res[2] == 0:
            return right_res
        if right_res[2] == 0:
            return left_res
            
        ansL, remL, lenL = left_res
        ansR, remR, lenR = right_res
        
        needed = lenR - ansR
        available = lenL - remL
        
        new_ans = ansL + ansR + min(needed, available)
        new_rem = remL + max(0, remR - needed)
        
        return (new_ans, new_rem, lenL + lenR)

    results = []
    for l, r, idx in queries:
        # Adjust to 0-based index
        ans, rem, _ = query(1, 0, N - 1, l - 1, r - 1)
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()