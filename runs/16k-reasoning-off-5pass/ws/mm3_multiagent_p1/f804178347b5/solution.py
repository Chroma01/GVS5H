import sys

def solve():
    data = sys.stdin.read().split()
    N = int(data[0])
    A = data[1].strip()
    
    # Recursive function: returns (dp0, dp1) for the segment A[l:r]
    # dp0 = min flips to make this segment's majority = 0
    # dp1 = min flips to make this segment's majority = 1
    def dfs(l, r):
        length = r - l
        if length == 1:
            # leaf
            if A[l] == '0':
                return (0, 1)  # already 0, need 1 flip to make 1
            else:
                return (1, 0)  # already 1, need 1 flip to make 0
        else:
            third = length // 3
            # three children
            c1 = dfs(l, l + third)
            c2 = dfs(l + third, l + 2 * third)
            c3 = dfs(l + 2 * third, r)
            
            # For target 0: need at least 2 children with value 0
            # Option 1: all three are 0
            cost_all_0 = c1[0] + c2[0] + c3[0]
            # Option 2: exactly two are 0, one is 1
            cost_two_0_a = c1[0] + c2[0] + c3[1]  # c3 is the odd one
            cost_two_0_b = c1[0] + c2[1] + c3[0]  # c2 is the odd one
            cost_two_0_c = c1[1] + c2[0] + c3[0]  # c1 is the odd one
            dp0 = min(cost_all_0, cost_two_0_a, cost_two_0_b, cost_two_0_c)
            
            # For target 1: need at least 2 children with value 1
            cost_all_1 = c1[1] + c2[1] + c3[1]
            cost_two_1_a = c1[1] + c2[1] + c3[0]
            cost_two_1_b = c1[1] + c2[0] + c3[1]
            cost_two_1_c = c1[0] + c2[1] + c3[1]
            dp1 = min(cost_all_1, cost_two_1_a, cost_two_1_b, cost_two_1_c)
            
            return (dp0, dp1)
    
    total_len = 3 ** N
    dp0, dp1 = dfs(0, total_len)
    
    # Determine current root value by simulating majority operations
    # Or: current value is the one with 0 cost (if dp0 == 0 then current is 0, etc.)
    # Actually dp0 is min flips to make it 0; if it's already 0, dp0 = 0.
    # So current value v satisfies dp_v == 0.
    if dp0 == 0:
        current = 0
    else:
        current = 1
    
    # We want to flip it, so target is 1 - current
    target = 1 - current
    if target == 0:
        print(dp0)
    else:
        print(dp1)

solve()