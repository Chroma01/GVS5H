import sys

def solve():
    # Increase recursion depth just in case, though we use iterative backtracking
    sys.setrecursionlimit(2000000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    ops = []
    for _ in range(M):
        L = int(next(iterator))
        R = int(next(iterator))
        ops.append((L, R))

    # dp[i] = min cost to make prefix 1..i all 1s
    # Initialize with infinity
    INF = 10**18
    dp = [INF] * (N + 1)
    dp[0] = 0
    
    # history[k] stores a dict: index -> (new_cost, prev_index, op_type)
    # prev_index is None if it came from global min (Op 2)
    history = [{} for _ in range(M + 1)]
    
    # global_min[k] stores the minimum value in dp array after step k
    global_min = [INF] * (M + 1)
    global_min[0] = 0
    
    # min_index[k] stores an index i such that dp[i] == global_min[k]
    min_index = [0] * (M + 1)
    
    for k in range(1, M + 1):
        L, R = ops[k-1]
        
        # Current dp state is from step k-1
        prev_dp = dp # Reference to current state before updates
        
        # Calculate potential new costs
        # Op 2: Sets 1..L-1 to 1. Cost = global_min[k-1] + 1
        # This updates dp[L-1]
        cost_op2 = global_min[k-1] + 1
        
        # Op 1: Sets L..R to 1. Extends coverage from L-1 to R.
        # Cost = dp[L-1] + 1
        # This updates dp[R]
        cost_op1 = prev_dp[L-1] + 1
        
        updates = {}
        
        # Apply Op 2 update if it improves dp[L-1]
        if cost_op2 < prev_dp[L-1]:
            updates[L-1] = (cost_op2, None, 2)
            dp[L-1] = cost_op2
            
        # Apply Op 1 update if it improves dp[R]
        if cost_op1 < prev_dp[R]:
            updates[R] = (cost_op1, L-1, 1)
            dp[R] = cost_op1
            
        history[k] = updates
        
        # Update global_min and min_index for step k
        # The new global min is min(global_min[k-1], min(values in updates))
        new_min = global_min[k-1]
        new_min_idx = min_index[k-1]
        
        if updates:
            for idx, (val, _, _) in updates.items():
                if val < new_min:
                    new_min = val
                    new_min_idx = idx
                elif val == new_min:
                    # Keep the existing one or pick any, doesn't matter for correctness
                    pass
        
        global_min[k] = new_min
        min_index[k] = new_min_idx

    if dp[N] == INF:
        print("-1")
    else:
        # Backtrack to find the operations
        chosen_ops = [0] * M
        curr_i = N
        
        for k in range(M, 0, -1):
            L, R = ops[k-1]
            hist = history[k]
            
            if curr_i in hist:
                new_cost, prev_i, op_type = hist[curr_i]
                chosen_ops[k-1] = op_type
                
                if op_type == 2:
                    # Came from global min at step k-1
                    curr_i = min_index[k-1]
                else:
                    # Came from specific previous state
                    curr_i = prev_i
            else:
                # No update for this state at this step, so Op 0 was effectively chosen
                # or this state wasn't part of the optimal path for this specific index
                # But since we are tracking the optimal path for curr_i, if it wasn't updated,
                # it means the value didn't change, so we assume Op 0.
                chosen_ops[k-1] = 0
                # curr_i remains the same
        
        print(dp[N])
        print(*(chosen_ops))

solve()