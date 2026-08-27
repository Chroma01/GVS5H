import sys

# Increase recursion depth just in case, though we use an iterative approach.
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    A = input_data[1]
    
    # Step 1: Determine the initial value of the root (A'_1) by simulating the reduction.
    # We start with the full string A and reduce it until length is 1.
    current_level = list(A)
    
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 3):
            group = current_level[i:i+3]
            # Majority vote: if '1' appears 2 or more times, result is '1', else '0'
            if group.count('1') >= 2:
                next_level.append('1')
            else:
                next_level.append('0')
        current_level = next_level
    
    initial_root_val = current_level[0]
    
    # Step 2: Dynamic Programming (Bottom-Up) to find minimum flips.
    # dp0[i] = min flips in the subtree rooted at node i (at current level) to make it '0'
    # dp1[i] = min flips in the subtree rooted at node i (at current level) to make it '1'
    
    # Initialize for the leaf level (level N).
    # The leaves correspond to the characters in A.
    # Cost to force a leaf to '0' is 1 if it's currently '1', else 0.
    # Cost to force a leaf to '1' is 1 if it's currently '0', else 0.
    dp0 = [1 if c == '1' else 0 for c in A]
    dp1 = [1 if c == '0' else 0 for c in A]
    
    # Iterate from level N-1 down to 0.
    # Level k has 3^k nodes. Level k+1 has 3^(k+1) nodes.
    # Node i at level k depends on nodes 3*i, 3*i+1, 3*i+2 at level k+1.
    current_len = len(A) # 3^N
    
    while current_len > 1:
        next_len = current_len // 3
        new_dp0 = [0] * next_len
        new_dp1 = [0] * next_len
        
        for i in range(next_len):
            c1 = 3 * i
            c2 = 3 * i + 1
            c3 = 3 * i + 2
            
            # To make node i '0', we need at least 2 children to be '0'.
            # We consider all pairs of children and take the minimum sum of costs.
            cost0_12 = dp0[c1] + dp0[c2]
            cost0_13 = dp0[c1] + dp0[c3]
            cost0_23 = dp0[c2] + dp0[c3]
            new_dp0[i] = min(cost0_12, cost0_13, cost0_23)
            
            # To make node i '1', we need at least 2 children to be '1'.
            cost1_12 = dp1[c1] + dp1[c2]
            cost1_13 = dp1[c1] + dp1[c3]
            cost1_23 = dp1[c2] + dp1[c3]
            new_dp1[i] = min(cost1_12, cost1_13, cost1_23)
            
        dp0 = new_dp0
        dp1 = new_dp1
        current_len = next_len
        
    # After the loop, we are at the root (level 0).
    # dp0[0] is the cost to make the root '0'.
    # dp1[0] is the cost to make the root '1'.
    
    if initial_root_val == '0':
        # We need to change it to '1'
        print(dp1[0])
    else:
        # We need to change it to '0'
        print(dp0[0])

if __name__ == '__main__':
    solve()