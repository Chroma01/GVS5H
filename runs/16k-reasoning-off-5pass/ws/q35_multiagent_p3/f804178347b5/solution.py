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
    
    # dp0[i] will store the min cost to make the i-th node at current level equal to 0
    # dp1[i] will store the min cost to make the i-th node at current level equal to 1
    # Initially, level 0 corresponds to the leaves (the input string A)
    
    dp0 = [0] * length
    dp1 = [0] * length
    
    for i in range(length):
        if A_str[i] == '0':
            dp0[i] = 0
            dp1[i] = 1
        else:
            dp0[i] = 1
            dp1[i] = 0
            
    # Iterate from level 1 to N
    # At each step, we reduce the number of nodes by a factor of 3
    current_len = length
    for level in range(1, N + 1):
        next_len = current_len // 3
        new_dp0 = [0] * next_len
        new_dp1 = [0] * next_len
        
        for i in range(next_len):
            # Children indices in the previous level's arrays
            c0_idx = 3 * i
            c1_idx = 3 * i + 1
            c2_idx = 3 * i + 2
            
            # Costs for children to be 0
            cost_c0_0 = dp0[c0_idx]
            cost_c1_0 = dp0[c1_idx]
            cost_c2_0 = dp0[c2_idx]
            
            # Costs for children to be 1
            cost_c0_1 = dp1[c0_idx]
            cost_c1_1 = dp1[c1_idx]
            cost_c2_1 = dp1[c2_idx]
            
            # To make current node 0, at least 2 children must be 0
            # Option 1: Children 0 and 1 are 0, Child 2 is min(0,1)
            opt1_0 = cost_c0_0 + cost_c1_0 + min(cost_c2_0, cost_c2_1)
            
            # Option 2: Children 0 and 2 are 0, Child 1 is min(0,1)
            opt2_0 = cost_c0_0 + cost_c2_0 + min(cost_c1_0, cost_c1_1)
            
            # Option 3: Children 1 and 2 are 0, Child 0 is min(0,1)
            opt3_0 = cost_c1_0 + cost_c2_0 + min(cost_c0_0, cost_c0_1)
            
            new_dp0[i] = min(opt1_0, opt2_0, opt3_0)
            
            # To make current node 1, at least 2 children must be 1
            # Option 1: Children 0 and 1 are 1, Child 2 is min(0,1)
            opt1_1 = cost_c0_1 + cost_c1_1 + min(cost_c2_0, cost_c2_1)
            
            # Option 2: Children 0 and 2 are 1, Child 1 is min(0,1)
            opt2_1 = cost_c0_1 + cost_c2_1 + min(cost_c1_0, cost_c1_1)
            
            # Option 3: Children 1 and 2 are 1, Child 0 is min(0,1)
            opt3_1 = cost_c1_1 + cost_c2_1 + min(cost_c0_0, cost_c0_1)
            
            new_dp1[i] = min(opt1_1, opt2_1, opt3_1)
            
        dp0 = new_dp0
        dp1 = new_dp1
        current_len = next_len
        
    # The root is at index 0 of the final level
    # The original value of the root can be determined by simulating or just checking
    # which cost is lower for the original configuration? 
    # Actually, we don't need the original value explicitly if we just output the cost to flip it.
    # The problem asks for min changes to CHANGE the value.
    # If original root is 0, we want cost to make it 1 -> dp1[0]
    # If original root is 1, we want cost to make it 0 -> dp0[0]
    
    # Let's determine the original root value by simulating the process on the original A
    # Or simpler: The cost to make root 0 is dp0[0], cost to make root 1 is dp1[0].
    # The original root value V is such that the cost to achieve V is 0? No, that's not right.
    # The DP computes min flips. The original configuration has a specific root value.
    # We can just simulate the majority operation on the original string A to find its root value.
    
    # Simulation of original A
    curr = list(A_str)
    while len(curr) > 1:
        next_curr = []
        for i in range(0, len(curr), 3):
            group = curr[i:i+3]
            if group.count('1') > group.count('0'):
                next_curr.append('1')
            else:
                next_curr.append('0')
        curr = next_curr
        
    original_root_val = curr[0]
    
    if original_root_val == '0':
        # We want to change it to 1
        print(dp1[0])
    else:
        # We want to change it to 0
        print(dp0[0])

if __name__ == '__main__':
    solve()