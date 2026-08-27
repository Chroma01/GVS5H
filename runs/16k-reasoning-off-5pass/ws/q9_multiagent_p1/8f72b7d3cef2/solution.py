import sys

# Increase recursion depth just in case, though iterative find is used.
sys.setrecursionlimit(2000000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    if N == 0:
        print()
        return

    # Prepare indices sorted by value A[i] ascending.
    # We store tuples (value, original_index) to handle sorting correctly.
    # Sorting by value ensures we process smaller slimes first.
    # If values are equal, the relative order doesn't strictly matter for correctness 
    # because equal values cannot absorb each other (strictly smaller condition).
    indices = sorted(range(N), key=lambda i: A[i])

    # DSU structures
    parent = list(range(N))
    # sum_comp[i] stores the sum of the component rooted at i
    sum_comp = list(A)
    
    # Iterative find with path compression to avoid recursion depth issues
    def find(i):
        root = i
        while root != parent[root]:
            root = parent[root]
        
        # Path compression
        curr = i
        while curr != root:
            nxt = parent[curr]
            parent[curr] = root
            curr = nxt
        return root

    ans = [0] * N

    # Iterate through slimes in increasing order of size
    for idx in indices:
        val = A[idx]
        
        # We start with the current slime's size.
        # We will try to merge with adjacent components if the adjacent slime 
        # (or the component it belongs to) is strictly smaller than the current slime.
        # Since we process in ascending order, any neighbor already in DSU has A[neighbor] <= A[idx].
        # If A[neighbor] < A[idx], we can absorb the entire component.
        
        # Check Left Neighbor
        if idx > 0:
            left_val = A[idx-1]
            if left_val < val:
                root_left = find(idx-1)
                root_idx = find(idx)
                if root_idx != root_left:
                    # Merge left component into current component
                    # We attach root_left to root_idx
                    parent[root_left] = root_idx
                    sum_comp[root_idx] += sum_comp[root_left]
        
        # Check Right Neighbor
        if idx < N - 1:
            right_val = A[idx+1]
            if right_val < val:
                root_right = find(idx+1)
                root_idx = find(idx)
                if root_idx != root_right:
                    # Merge right component into current component
                    parent[root_right] = root_idx
                    sum_comp[root_idx] += sum_comp[root_right]
        
        # The answer for the slime at 'idx' is the sum of the component it belongs to.
        # Note: Since we might have merged into 'idx' (or 'idx' merged into others),
        # we must find the root of 'idx' to get the correct total sum.
        root_final = find(idx)
        ans[idx] = sum_comp[root_final]

    # Print results separated by spaces
    print(*(ans))

if __name__ == '__main__':
    solve()