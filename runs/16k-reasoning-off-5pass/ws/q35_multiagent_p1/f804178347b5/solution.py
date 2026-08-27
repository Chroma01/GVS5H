import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    A_str = input_data[1]
    
    # Length of the string is 3^N
    length = 3**N
    
    # Convert string to list of integers for easier handling
    # A[i] is the i-th character (0-indexed)
    A = [int(c) for c in A_str]
    
    # dp[b] will store the cost for the current level's blocks to reduce to bit b
    # At level 0, we have 'length' blocks of size 1.
    # dp[0][i] = cost to make A[i] reduce to 0
    # dp[1][i] = cost to make A[i] reduce to 1
    
    # Initialize for level 0
    # costs[i][0] is cost to make block i at current level reduce to 0
    # costs[i][1] is cost to make block i at current level reduce to 1
    costs = [[0, 0] for _ in range(length)]
    
    for i in range(length):
        val = A[i]
        costs[i][0] = 1 - val  # Cost to make it 0
        costs[i][1] = val      # Cost to make it 1
        
    # Iterate from level 1 to N
    # At each level k, the number of blocks is 3^(N-k)
    # Each block at level k is formed by 3 blocks from level k-1
    for k in range(1, N + 1):
        prev_length = length // (3**(k-1))
        curr_length = length // (3**k)
        
        new_costs = [[0, 0] for _ in range(curr_length)]
        
        for j in range(curr_length):
            # The j-th block at level k consists of sub-blocks:
            # 3*j, 3*j+1, 3*j+2 from the previous level
            idx0 = 3 * j
            idx1 = 3 * j + 1
            idx2 = 3 * j + 2
            
            # Get costs from previous level
            c0_0 = costs[idx0][0]
            c0_1 = costs[idx0][1]
            c1_0 = costs[idx1][0]
            c1_1 = costs[idx1][1]
            c2_0 = costs[idx2][0]
            c2_1 = costs[idx2][1]
            
            # Calculate cost to make current block reduce to 0
            # Need at least 2 sub-blocks to reduce to 0
            # Option 1: 0, 0, 1
            opt1 = c0_0 + c1_0 + c2_1
            # Option 2: 0, 1, 0
            opt2 = c0_0 + c1_1 + c2_0
            # Option 3: 1, 0, 0
            opt3 = c0_1 + c1_0 + c2_0
            
            new_costs[j][0] = min(opt1, opt2, opt3)
            
            # Calculate cost to make current block reduce to 1
            # Need at least 2 sub-blocks to reduce to 1
            # Option 1: 1, 1, 0
            opt4 = c0_1 + c1_1 + c2_0
            # Option 2: 1, 0, 1
            opt5 = c0_1 + c1_0 + c2_1
            # Option 3: 0, 1, 1
            opt6 = c0_0 + c1_1 + c2_1
            
            new_costs[j][1] = min(opt4, opt5, opt6)
            
        costs = new_costs
        length = curr_length
        
    # The final result is at index 0 of the last level
    # Determine the original final result
    # We can compute it by simulating the process or just checking which target was cheaper
    # Actually, we need to know what the original result was to know what to flip TO.
    # Let's compute the original result by simulating the reduction on the original string A.
    
    # Simulate original reduction
    current_A = A
    for _ in range(N):
        new_A = []
        for i in range(0, len(current_A), 3):
            group = current_A[i:i+3]
            if group.count(1) > group.count(0):
                new_A.append(1)
            else:
                new_A.append(0)
        current_A = new_A
        
    original_final = current_A[0]
    
    # If original final is 0, we want to change it to 1 -> cost is costs[0][1]
    # If original final is 1, we want to change it to 0 -> cost is costs[0][0]
    
    if original_final == 0:
        print(costs[0][1])
    else:
        print(costs[0][0])

solve()