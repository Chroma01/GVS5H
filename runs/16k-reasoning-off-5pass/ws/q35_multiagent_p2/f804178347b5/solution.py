import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A_str = input_data[1]
    
    # A is a string of '0's and '1's
    # We will work with lists of integers for DP
    # dp0[i] = min cost to make the i-th element at current level evaluate to 0
    # dp1[i] = min cost to make the i-th element at current level evaluate to 1
    
    # Level 0: leaves
    # For each leaf, cost to be 0 is 1 if A[i]=='1' else 0
    # Cost to be 1 is 1 if A[i]=='0' else 0
    
    dp0 = [1 if c == '1' else 0 for c in A_str]
    dp1 = [1 if c == '0' else 0 for c in A_str]
    
    # Current length of the array
    current_len = len(dp0)
    
    # We need to apply the operation N times
    # Each time, the length becomes 1/3
    for _ in range(N):
        new_len = current_len // 3
        new_dp0 = [0] * new_len
        new_dp1 = [0] * new_len
        
        for i in range(new_len):
            # The i-th group consists of indices 3*i, 3*i+1, 3*i+2
            idx0 = 3 * i
            idx1 = 3 * i + 1
            idx2 = 3 * i + 2
            
            # To make the parent 0, we need at least 2 children to be 0
            # Options:
            # 1. All 3 children are 0: cost = dp0[idx0] + dp0[idx1] + dp0[idx2]
            # 2. Two children are 0, one is 1: 
            #    We pick the two cheapest dp0 and the cheapest dp1 for the third?
            #    Actually, we just need to choose states for the 3 children such that at least 2 are 0.
            #    The cost is sum of costs for chosen states.
            #    Let c0_0, c0_1, c0_2 be dp0 for the three children
            #    Let c1_0, c1_1, c1_2 be dp1 for the three children
            #    We want to minimize sum of chosen costs with at least 2 zeros.
            #    This is equivalent to:
            #    min(
            #        c0_0 + c0_1 + c0_2,  # all 0
            #        c0_0 + c0_1 + c1_2,  # 0,0,1
            #        c0_0 + c1_1 + c0_2,  # 0,1,0
            #        c1_0 + c0_1 + c0_2   # 1,0,0
            #    )
            #    Which is: c0_0 + c0_1 + c0_2 is one option.
            #    The other options are: take two c0's and one c1.
            #    To minimize, we should take the two smallest c0's and the smallest c1?
            #    No, we take two c0's and one c1. The cost is sum of two c0's + one c1.
            #    We want to minimize this over all choices of which child is 1.
            #    So: min( c0_0 + c0_1 + c1_2, c0_0 + c1_1 + c0_2, c1_0 + c0_1 + c0_2 )
            #    And also compare with all 0s.
            
            # Let's compute all 4 costs explicitly for clarity and correctness
            cost_all_0 = dp0[idx0] + dp0[idx1] + dp0[idx2]
            cost_001 = dp0[idx0] + dp0[idx1] + dp1[idx2]
            cost_010 = dp0[idx0] + dp1[idx1] + dp0[idx2]
            cost_100 = dp1[idx0] + dp0[idx1] + dp0[idx2]
            
            new_dp0[i] = min(cost_all_0, cost_001, cost_010, cost_100)
            
            # Similarly for making the parent 1 (at least 2 children are 1)
            cost_all_1 = dp1[idx0] + dp1[idx1] + dp1[idx2]
            cost_110 = dp1[idx0] + dp1[idx1] + dp0[idx2]
            cost_101 = dp1[idx0] + dp0[idx1] + dp1[idx2]
            cost_011 = dp0[idx0] + dp1[idx1] + dp1[idx2]
            
            new_dp1[i] = min(cost_all_1, cost_110, cost_101, cost_011)
            
        dp0 = new_dp0
        dp1 = new_dp1
        current_len = new_len
        
    # After N steps, we have one element at the root
    # dp0[0] is the min cost to make the root 0
    # dp1[0] is the min cost to make the root 1
    
    # We need to determine the original value of the root
    # We can simulate the majority operation on the original string A
    # Or we can note that the original root value is determined by the initial A.
    # Let's simulate it quickly.
    
    current_A = [int(c) for c in A_str]
    for _ in range(N):
        new_len = len(current_A) // 3
        next_A = []
        for i in range(new_len):
            g = current_A[3*i : 3*i+3]
            # majority
            if g.count(1) >= 2:
                next_A.append(1)
            else:
                next_A.append(0)
        current_A = next_A
        
    original_root = current_A[0]
    
    if original_root == 0:
        # We want to flip to 1, so the cost is dp1[0]
        print(dp1[0])
    else:
        # We want to flip to 0, so the cost is dp0[0]
        print(dp0[0])

solve()