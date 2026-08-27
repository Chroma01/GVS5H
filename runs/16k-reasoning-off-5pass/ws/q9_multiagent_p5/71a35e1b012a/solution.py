import sys
import heapq

# Increase recursion depth just in case, though iterative approach is used
sys.setrecursionlimit(300005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Store operations
    L = []
    R = []
    for _ in range(M):
        L.append(int(next(iterator)))
        R.append(int(next(iterator)))

    # If M=0, impossible unless N=0 (not possible per constraints).
    if M == 0:
        print("-1")
        return

    # DSU initialization
    # parent[i] points to the next uncovered position >= i
    parent = list(range(N + 2))
    
    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i
    
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j

    # Precompute min_R_less
    # min_R_less_val[x] = min R[i] such that R[i] < x
    # min_R_less_idx[x] = index of op with that R
    INF = N + 1
    min_R_less_val = [INF] * (N + 2)
    min_R_less_idx = [-1] * (N + 2)
    
    for i in range(M):
        r_val = R[i]
        if r_val < N + 1:
            if r_val < min_R_less_val[r_val + 1]:
                min_R_less_val[r_val + 1] = r_val
                min_R_less_idx[r_val + 1] = i
    
    # Prefix min
    current_min = INF
    current_idx = -1
    for i in range(1, N + 2):
        if min_R_less_val[i] < current_min:
            current_min = min_R_less_val[i]
            current_idx = min_R_less_idx[i]
        min_R_less_val[i] = current_min
        min_R_less_idx[i] = current_idx
        
    # Precompute max_L_ge
    # max_L_ge_val[x] = max L[i] such that L[i] >= x
    # max_L_ge_idx[x] = index of op with that L
    max_L_ge_val = [INF] * (N + 2)
    max_L_ge_idx = [-1] * (N + 2)
    
    for i in range(M):
        l_val = L[i]
        if l_val <= N:
            if l_val > max_L_ge_val[l_val]:
                max_L_ge_val[l_val] = l_val
                max_L_ge_idx[l_val] = i
                
    # Suffix max
    current_max = INF
    current_idx = -1
    for i in range(N, 0, -1):
        if max_L_ge_val[i] > current_max:
            current_max = max_L_ge_val[i]
            current_idx = max_L_ge_idx[i]
        max_L_ge_val[i] = current_max
        max_L_ge_idx[i] = current_idx

    # Sort ops by L
    ops_by_L = sorted(range(M), key=lambda i: L[i])
    
    # Max-heap for R values (store -R for max-heap behavior)
    heap_R = [] # stores (-R, i)
    ptr_L = 0
    
    # Result array
    res_ops = [0] * M
    
    curr = 1
    while curr <= N:
        curr = find(curr)
        if curr > N:
            break
            
        # Find best Type 1
        # Add ops with L[i] <= curr
        while ptr_L < M and L[ops_by_L[ptr_L]] <= curr:
            idx = ops_by_L[ptr_L]
            heapq.heappush(heap_R, (-R[idx], idx))
            ptr_L += 1
            
        best_R1 = -1
        best_idx1 = -1
        while heap_R:
            neg_r, idx = heap_R[0]
            r_val = -neg_r
            if r_val >= curr:
                best_R1 = r_val
                best_idx1 = idx
                break
            else:
                heapq.heappop(heap_R)
        
        # Type 2a (curr > R[i]) -> covers [R[i]+1, N]
        min_r_2a = min_R_less_val[curr]
        best_idx2a = -1
        if min_r_2a < curr:
            best_idx2a = min_R_less_idx[curr]
            
        # Type 2b (curr < L[i]) -> covers [curr, L[i]-1]
        max_l_2b = max_L_ge_val[curr+1]
        best_idx2b = -1
        if max_l_2b > curr:
            best_idx2b = max_L_ge_idx[curr+1]
            
        # Compare
        candidates = []
        if best_R1 != -1:
            candidates.append((best_R1, 1, best_idx1))
        if min_r_2a < curr:
            candidates.append((N, 2, best_idx2a))
        if max_l_2b > curr:
            candidates.append((max_l_2b - 1, 2, best_idx2b))
            
        if not candidates:
            print("-1")
            return
        
        # Sort by reach descending
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_reach, type_choice, op_idx = candidates[0]
        
        res_ops[op_idx] = type_choice
        
        # Update DSU
        # We cover up to best_reach. The next uncovered starts at best_reach + 1.
        if best_reach + 1 <= N:
            union(curr, best_reach + 1)
        else:
            union(curr, N + 1)
            
        # Move curr to next uncovered
        curr = find(curr)
        
    # Count non-zero operations
    cost = sum(1 for x in res_ops if x != 0)
    print(cost)
    print(*(res_ops))

if __name__ == '__main__':
    solve()