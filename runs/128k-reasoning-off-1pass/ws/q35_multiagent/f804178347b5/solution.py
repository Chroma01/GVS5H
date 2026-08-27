import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A_str = input_data[1]
    
    # Total length is 3^N
    length = 3**N
    
    # dp[i] will store (cost0, cost1) for the i-th node at the current level
    # Initially, for leaves (level 0)
    dp = []
    for char in A_str:
        if char == '0':
            dp.append((0, 1))  # cost to make it 0 is 0, to make it 1 is 1
        else:
            dp.append((1, 0))  # cost to make it 1 is 0, to make it 0 is 1
            
    # Iteratively compute costs for each level up to the root
    # There are N levels of operations
    for level in range(N):
        new_dp = []
        # Process groups of 3
        for i in range(0, len(dp), 3):
            c0_0, c0_1 = dp[i]
            c1_0, c1_1 = dp[i+1]
            c2_0, c2_1 = dp[i+2]
            
            # To make majority 0: need at least 2 children to be 0
            # Option 1: children 0 and 1 are 0, child 2 can be anything (take min cost)
            opt1 = c0_0 + c1_0 + min(c2_0, c2_1)
            # Option 2: children 0 and 2 are 0, child 1 can be anything
            opt2 = c0_0 + c2_0 + min(c1_0, c1_1)
            # Option 3: children 1 and 2 are 0, child 0 can be anything
            opt3 = c1_0 + c2_0 + min(c0_0, c0_1)
            
            cost0 = min(opt1, opt2, opt3)
            
            # To make majority 1: need at least 2 children to be 1
            opt1 = c0_1 + c1_1 + min(c2_0, c2_1)
            opt2 = c0_1 + c2_1 + min(c1_0, c1_1)
            opt3 = c1_1 + c2_1 + min(c0_0, c0_1)
            
            cost1 = min(opt1, opt2, opt3)
            
            new_dp.append((cost0, cost1))
            
        dp = new_dp
        
    # dp[0] now contains (cost0, cost1) for the root
    cost0, cost1 = dp[0]
    
    # Determine the original final value
    # We can simulate the process on the original string to find the original value
    # Or we can note that the original value is the one with 0 cost to maintain
    # But due to the nature of the problem, one of cost0 or cost1 should be 0 for the root
    # if we consider the original configuration. However, let's simulate to be safe.
    
    # Simulate the original process
    current = list(A_str)
    for _ in range(N):
        new_current = []
        for i in range(0, len(current), 3):
            group = current[i:i+3]
            # Majority vote
            if group.count('1') > group.count('0'):
                new_current.append('1')
            else:
                new_current.append('0')
        current = new_current
        
    original_value = current[0]
    
    if original_value == '0':
        # We want to change it to 1, so we need cost1 changes
        print(cost1)
    else:
        # We want to change it to 0, so we need cost0 changes
        print(cost0)

solve()