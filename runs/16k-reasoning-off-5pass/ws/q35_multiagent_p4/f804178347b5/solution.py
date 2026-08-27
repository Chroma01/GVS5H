import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    A_str = input_data[1]
    
    # Length of the string is 3^N
    # We will compute DP tables bottom-up.
    # dp0[k] will store the min cost for the k-th block at current level to evaluate to 0
    # dp1[k] will store the min cost for the k-th block at current level to evaluate to 1
    
    # Level 0: Leaves, there are 3^N leaves
    num_leaves = 3**N
    dp0 = [0] * num_leaves
    dp1 = [0] * num_leaves
    
    for i in range(num_leaves):
        if A_str[i] == '0':
            dp0[i] = 0
            dp1[i] = 1
        else:
            dp0[i] = 1
            dp1[i] = 0
            
    # Iterate from level 1 to N
    # At level k, there are 3^(N-k) blocks
    for k in range(1, N + 1):
        prev_size = 3**(N - k + 1)
        curr_size = 3**(N - k)
        
        new_dp0 = [0] * curr_size
        new_dp1 = [0] * curr_size
        
        for i in range(curr_size):
            # Children indices in the previous level's arrays
            c1_idx = 3 * i
            c2_idx = 3 * i + 1
            c3_idx = 3 * i + 2
            
            # Costs for children to be 0 or 1
            c1_0 = dp0[c1_idx]
            c1_1 = dp1[c1_idx]
            c2_0 = dp0[c2_idx]
            c2_1 = dp1[c2_idx]
            c3_0 = dp0[c3_idx]
            c3_1 = dp1[c3_idx]
            
            # Calculate cost to make current block 1
            # Need at least two children to be 1
            # Combinations: (1,1,0), (1,0,1), (0,1,1), (1,1,1)
            cost_1_1_0 = c1_1 + c2_1 + c3_0
            cost_1_0_1 = c1_1 + c2_0 + c3_1
            cost_0_1_1 = c1_0 + c2_1 + c3_1
            cost_1_1_1 = c1_1 + c2_1 + c3_1
            
            new_dp1[i] = min(cost_1_1_0, cost_1_0_1, cost_0_1_1, cost_1_1_1)
            
            # Calculate cost to make current block 0
            # Need at least two children to be 0
            # Combinations: (0,0,1), (0,1,0), (1,0,0), (0,0,0)
            cost_0_0_1 = c1_0 + c2_0 + c3_1
            cost_0_1_0 = c1_0 + c2_1 + c3_0
            cost_1_0_0 = c1_1 + c2_0 + c3_0
            cost_0_0_0 = c1_0 + c2_0 + c3_0
            
            new_dp0[i] = min(cost_0_0_1, cost_0_1_0, cost_1_0_0, cost_0_0_0)
            
        dp0 = new_dp0
        dp1 = new_dp1
        
    # The root is at index 0 of the final dp arrays
    # Determine the original value of the root
    # If dp1[0] == 0, original is 1. If dp0[0] == 0, original is 0.
    # We want to change the value, so if original is 1, we need cost to make it 0 (dp0[0])
    # If original is 0, we need cost to make it 1 (dp1[0])
    
    if dp1[0] == 0:
        # Original is 1, want to make it 0
        print(dp0[0])
    else:
        # Original is 0, want to make it 1
        print(dp1[0])

solve()