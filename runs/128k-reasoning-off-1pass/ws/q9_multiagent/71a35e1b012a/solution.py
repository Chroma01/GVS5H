import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
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

    # List of (L, R, original_index) for Op 1 candidates
    op1_candidates = []
    
    # List of (L, original_index) for Op 2 candidates
    op2_candidates = []
    
    for i in range(M):
        try:
            L = int(next(iterator))
            R = int(next(iterator))
            op1_candidates.append((L, R, i))
            op2_candidates.append((L, i))
        except StopIteration:
            break
            
    # Precompute best_R1[u]: max R_i such that L_i <= u
    # We also store the corresponding op_index to reconstruct the path
    # best_R1_info[u] = (max_R, op_index)
    
    op1_candidates.sort(key=lambda x: x[0])
    
    best_R1_info = [(0, -1)] * (N + 2)
    current_max_R = 0
    current_op_idx = -1
    idx = 0
    num_ops = len(op1_candidates)
    
    # Fill best_R1
    for u in range(1, N + 2):
        while idx < num_ops and op1_candidates[idx][0] <= u:
            R = op1_candidates[idx][1]
            op_id = op1_candidates[idx][2]
            if R > current_max_R:
                current_max_R = R
                current_op_idx = op_id
            idx += 1
        best_R1_info[u] = (current_max_R, current_op_idx)
        
    # Prepare Op 2 candidates for BFS
    # Sort by L.
    op2_candidates.sort(key=lambda x: x[0])
    
    # BFS Initialization
    # Nodes are 1 to N+1.
    # dist[u] = min cost to reach state u (where u is the first uncovered index)
    # parent[u] = (prev_u, op_type, op_index) to reconstruct path
    
    dist = [-1] * (N + 2)
    parent = [None] * (N + 2)
    
    queue = deque()
    queue.append(1)
    dist[1] = 0
    
    # Pointer for op2_candidates
    ptr = 0
    num_op2 = len(op2_candidates)
    
    while queue:
        u = queue.popleft()
        
        if u == N + 1:
            break
            
        # --- Try Operation 1 ---
        # We can transition to best_R1[u] + 1
        # Condition: L_i <= u is satisfied by definition of best_R1[u]
        # We also need R >= u to actually cover u.
        max_r, op_id = best_R1_info[u]
        
        if max_r >= u:
            target_u1 = max_r + 1
            if target_u1 <= N + 1 and dist[target_u1] == -1:
                dist[target_u1] = dist[u] + 1
                parent[target_u1] = (u, 1, op_id)
                queue.append(target_u1)
        
        # --- Try Operation 2 ---
        # We can transition to any L_i such that L_i > u.
        # We use the sorted list and pointer.
        while ptr < num_op2 and op2_candidates[ptr][0] > u:
            v = op2_candidates[ptr][0]
            op_idx = op2_candidates[ptr][1]
            
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                parent[v] = (u, 2, op_idx)
                queue.append(v)
            
            # Since we process u in increasing order of distance, and the set of valid L_i > u
            # shrinks as u increases, we can safely increment the pointer.
            # If v was already visited, it was reached via a shorter or equal path from a smaller u.
            ptr += 1
            
    if dist[N + 1] == -1:
        print("-1")
    else:
        print(dist[N + 1])
        # Reconstruct path
        # We need to fill result_ops.
        result_ops = [0] * M
        curr = N + 1
        while curr != 1:
            prev_u, op_type, op_idx = parent[curr]
            result_ops[op_idx] = op_type
            curr = prev_u
            
        print(" ".join(map(str, result_ops)))

if __name__ == '__main__':
    solve()