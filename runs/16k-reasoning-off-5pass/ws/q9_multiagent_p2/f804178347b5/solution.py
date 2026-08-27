import sys

# Increase recursion depth just in case, though we use an iterative approach.
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    A_str = input_data[1]
    
    length = 3 ** N
    
    # We will process the tree level by level from bottom (leaves) to top (root).
    # The leaves are at level N (indices 0 to 3^N - 1).
    # The root is at level 0.
    # We need to store the cost to flip the value of each node to 0 or 1.
    # Since we process bottom-up, we can store the costs for the current level
    # and compute the costs for the next level up.
    
    # Initialize costs for the leaves (level N).
    # cost[0] = cost to make this leaf 0
    # cost[1] = cost to make this leaf 1
    # If A[i] == '0', cost to make it 0 is 0, cost to make it 1 is 1.
    # If A[i] == '1', cost to make it 0 is 1, cost to make it 1 is 0.
    
    # We use a list of lists for the current level costs: [cost_to_0, cost_to_1]
    # Initially for leaves.
    
    # Current level size
    current_size = length
    
    # Initialize leaf costs
    level_costs = []
    
    for i in range(length):
        if A_str[i] == '0':
            level_costs.append([0, 1])
        else:
            level_costs.append([1, 0])
            
    # Iterate from level N-1 down to 1 (since we stop when we have the root at level 0)
    # In each step, we reduce the size by a factor of 3.
    # The number of nodes at level k is 3^k.
    # We start with size = 3^N, next size = 3^(N-1), ..., until size = 3^1 = 3.
    # After the loop, we will have the costs for the root (size=1).
    
    while current_size > 1:
        next_size = current_size // 3
        next_level_costs = []
        
        # Process each node in the current level (which are parents of the next level down)
        # Wait, the logic is:
        # We have costs for the children (current_size nodes).
        # We want to compute costs for the parents (next_size nodes).
        # Each parent has 3 children.
        
        for i in range(next_size):
            # Indices of children in the current level_costs list
            c1_idx = i * 3
            c2_idx = i * 3 + 1
            c3_idx = i * 3 + 2
            
            c1 = level_costs[c1_idx] # [cost_0, cost_1]
            c2 = level_costs[c2_idx]
            c3 = level_costs[c3_idx]
            
            # To make the parent 0, we need at least 2 children to be 0.
            # Combinations: (0,0,0), (0,0,1), (0,1,0), (1,0,0)
            cost_to_0 = min(
                c1[0] + c2[0] + c3[0],
                c1[0] + c2[0] + c3[1],
                c1[0] + c2[1] + c3[0],
                c1[1] + c2[0] + c3[0]
            )
            
            # To make the parent 1, we need at least 2 children to be 1.
            # Combinations: (1,1,1), (1,1,0), (1,0,1), (0,1,1)
            cost_to_1 = min(
                c1[1] + c2[1] + c3[1],
                c1[1] + c2[1] + c3[0],
                c1[1] + c2[0] + c3[1],
                c1[0] + c2[1] + c3[1]
            )
            
            next_level_costs.append([cost_to_0, cost_to_1])
            
        level_costs = next_level_costs
        current_size = next_size
        
    # Now level_costs contains the costs for the root.
    # The root's current value is determined by the majority of the original string's groups?
    # No, the problem asks to change the value of A'_1.
    # We need to know the current value of A'_1 to know what we are flipping it TO.
    # Actually, the DP state [cost_to_0, cost_to_1] tells us the cost to force the root to be 0 or 1.
    # The question is "minimum number of elements ... to change the value of A'_1".
    # So if A'_1 is currently 0, we need cost_to_1.
    # If A'_1 is currently 1, we need cost_to_0.
    
    # We need to determine the current value of the root.
    # We can simulate the process once on the original string A.
    
    current_val = A_str
    for _ in range(N):
        next_val = []
        for i in range(0, len(current_val), 3):
            group = current_val[i:i+3]
            # Majority
            if group.count('1') >= 2:
                next_val.append('1')
            else:
                next_val.append('0')
        current_val = "".join(next_val)
        
    target_val = '1' if current_val == '0' else '0'
    
    # The cost to flip the root to target_val
    root_costs = level_costs[0]
    if target_val == '0':
        print(root_costs[0])
    else:
        print(root_costs[1])

if __name__ == '__main__':
    solve()