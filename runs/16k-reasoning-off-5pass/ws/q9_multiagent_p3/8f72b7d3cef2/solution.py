import sys

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(2000000)

def solve():
    # Read all input from stdin
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

    # Precompute prefix sums for O(1) range sum queries
    # P[i] will store sum(A[0]...A[i-1])
    # Sum(A[l]...A[r]) = P[r+1] - P[l]
    P = [0] * (N + 1)
    for i in range(N):
        P[i+1] = P[i] + A[i]

    def get_sum(l, r):
        # Sum of A[l]...A[r] inclusive (0-based indices)
        if l > r:
            return 0
        return P[r+1] - P[l]

    # Compute L[i]: nearest index to the left such that A[L[i]] >= A[i]
    # If no such index exists, L[i] = -1
    L = [-1] * N
    stack = [] # Stores indices, values will be increasing
    for i in range(N):
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        if stack:
            L[i] = stack[-1]
        else:
            L[i] = -1
        stack.append(i)

    # Compute R[i]: nearest index to the right such that A[R[i]] >= A[i]
    # If no such index exists, R[i] = N
    R = [N] * N
    stack = []
    for i in range(N-1, -1, -1):
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        if stack:
            R[i] = stack[-1]
        else:
            R[i] = N
        stack.append(i)

    # The problem asks for the maximum size Takahashi can reach starting from each position K.
    # This is equivalent to finding the maximal contiguous range [l, r] containing K such that
    # for all k in [l, r], the sum of the subsegment is sufficient to absorb the boundaries.
    #
    # Specifically, the reachable range [l, r] for a starting position i is determined by:
    # 1. The first index j < i such that A[j] >= sum(j+1 ... i). If such j exists, l = j + 1. Else l = 0.
    # 2. The first index j > i such that A[j] >= sum(i ... j-1). If such j exists, r = j - 1. Else r = N - 1.
    #
    # These conditions can be rewritten using prefix sums:
    # 1. A[j] >= P[i+1] - P[j+1]  =>  P[j+1] + A[j] >= P[i+1].
    #    Let B[j] = P[j+1] + A[j]. We need the largest j < i such that B[j] >= P[i+1].
    # 2. A[j] >= P[j] - P[i]      =>  P[j] - A[j] <= P[i].
    #    Let D[j] = P[j] - A[j]. We need the smallest j > i such that D[j] <= P[i].
    
    # Precompute B and D arrays
    B = [0] * N
    D = [0] * N
    for j in range(N):
        B[j] = P[j+1] + A[j]
        D[j] = P[j] - A[j]

    # Build Segment Tree 1 (Max) for B to query largest index j < i with B[j] >= X
    size1 = 1
    while size1 < N:
        size1 *= 2
    tree1 = [float('-inf')] * (2 * size1)
    for j in range(N):
        tree1[size1 + j] = B[j]
    for i in range(size1 - 1, 0, -1):
        tree1[i] = max(tree1[2*i], tree1[2*i+1])

    # Build Segment Tree 2 (Min) for D to query smallest index j > i with D[j] <= X
    size2 = 1
    while size2 < N:
        size2 *= 2
    tree2 = [float('inf')] * (2 * size2)
    for j in range(N):
        tree2[size2 + j] = D[j]
    for i in range(size2 - 1, 0, -1):
        tree2[i] = min(tree2[2*i], tree2[2*i+1])

    def query_left(i, X):
        # Find largest j < i such that B[j] >= X
        if i == 0:
            return -1
        
        # Decompose range [0, i-1] into canonical nodes
        l, r = 0, i - 1
        l += size1
        r += size1
        nodes = []
        while l <= r:
            if l % 2 == 1:
                nodes.append(l)
                l += 1
            if r % 2 == 0:
                nodes.append(r)
                r -= 1
            l //= 2
            r //= 2
        
        # We want the largest index, so we check nodes from right to left (largest index first)
        # nodes list is not necessarily sorted by index, so we sort descending
        nodes.sort(reverse=True)
        
        target_node = -1
        for node in nodes:
            if tree1[node] >= X:
                target_node = node
                break
        
        if target_node == -1:
            return -1
        
        # Descend into target_node to find the rightmost leaf with value >= X
        curr = target_node
        while curr < size1:
            right_child = 2 * curr + 1
            if right_child < 2 * size1 and tree1[right_child] >= X:
                curr = right_child
            else:
                curr = 2 * curr
        
        return curr - size1

    def query_right(i, X):
        # Find smallest j > i such that D[j] <= X
        if i == N - 1:
            return N
        
        # Decompose range [i+1, N-1] into canonical nodes
        l, r = i + 1, N - 1
        l += size2
        r += size2
        nodes = []
        while l <= r:
            if l % 2 == 1:
                nodes.append(l)
                l += 1
            if r % 2 == 0:
                nodes.append(r)
                r -= 1
            l //= 2
            r //= 2
        
        # We want the smallest index, so we check nodes from left to right (smallest index first)
        nodes.sort()
        
        target_node = -1
        for node in nodes:
            if tree2[node] <= X:
                target_node = node
                break
        
        if target_node == -1:
            return N
        
        # Descend into target_node to find the smallest leaf with value <= X
        curr = target_node
        while curr < size2:
            left_child = 2 * curr
            if left_child < 2 * size2 and tree2[left_child] <= X:
                curr = left_child
            else:
                curr = 2 * curr + 1
        
        return curr - size2

    ans = [0] * N
    
    for i in range(N):
        # Find left boundary
        j = query_left(i, P[i+1])
        if j == -1:
            l_reach = 0
        else:
            l_reach = j + 1
        
        # Find right boundary
        j = query_right(i, P[i])
        if j == N:
            r_reach = N - 1
        else:
            r_reach = j - 1
        
        # Calculate sum
        ans[i] = get_sum(l_reach, r_reach)

    # Print result
    print(*(ans))

if __name__ == '__main__':
    solve()