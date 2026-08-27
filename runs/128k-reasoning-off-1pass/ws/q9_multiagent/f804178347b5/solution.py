import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    A = input_data[1]
    
    # Length of the string
    L = 3 ** N
    
    # We will process the string level by level from the bottom (leaves) to the top (root).
    # At each level, we compute the cost to flip the value of each node in that level to 0 or 1.
    # current_costs[k][0] = min flips to make node k at current level equal to '0'
    # current_costs[k][1] = min flips to make node k at current level equal to '1'
    
    # Initialize for leaves (level 0)
    # If A[i] == '0', cost to make it 0 is 0, cost to make it 1 is 1.
    # If A[i] == '1', cost to make it 0 is 1, cost to make it 1 is 0.
    
    current_costs = []
    for char in A:
        if char == '0':
            current_costs.append((0, 1))
        else:
            current_costs.append((1, 0))
            
    # Iterate from level 1 to N
    for level in range(1, N + 1):
        next_costs = []
        num_nodes = len(current_costs) // 3
        
        # Process each node at the next level up
        for i in range(num_nodes):
            # Children indices in current_costs
            c1 = i * 3
            c2 = c1 + 1
            c3 = c1 + 2
            
            cost0_1, cost1_1 = current_costs[c1]
            cost0_2, cost1_2 = current_costs[c2]
            cost0_3, cost1_3 = current_costs[c3]
            
            # To make the parent '0', we need at least 2 children to be '0'.
            # We evaluate all 4 combinations where at least 2 children are 0.
            # (0,0,0), (0,0,1), (0,1,0), (1,0,0)
            
            val1 = cost0_1 + cost0_2 + cost0_3
            val2 = cost0_1 + cost0_2 + cost1_3
            val3 = cost0_1 + cost1_2 + cost0_3
            val4 = cost1_1 + cost0_2 + cost0_3
            
            cost_to_0 = min(val1, val2, val3, val4)
            
            # To make the parent '1', we need at least 2 children to be '1'.
            # We evaluate all 4 combinations where at least 2 children are 1.
            # (1,1,1), (1,1,0), (1,0,1), (0,1,1)
            
            val5 = cost1_1 + cost1_2 + cost1_3
            val6 = cost1_1 + cost1_2 + cost0_3
            val7 = cost1_1 + cost0_2 + cost1_3
            val8 = cost0_1 + cost1_2 + cost1_3
            
            cost_to_1 = min(val5, val6, val7, val8)
            
            next_costs.append((cost_to_0, cost_to_1))
            
        current_costs = next_costs
        
    # After N levels, current_costs has 1 element: (cost_to_make_root_0, cost_to_make_root_1)
    cost_to_0, cost_to_1 = current_costs[0]
    
    # Determine the natural value of the root by simulating the majority operation on A
    curr = list(A)
    for _ in range(N):
        new_curr = []
        for i in range(0, len(curr), 3):
            s = curr[i] + curr[i+1] + curr[i+2]
            cnt1 = s.count('1')
            if cnt1 >= 2:
                new_curr.append('1')
            else:
                new_curr.append('0')
        curr = new_curr
        
    root_val = curr[0]
    
    # If the natural root value is '0', we need to flip it to '1' (cost = cost_to_1)
    # If the natural root value is '1', we need to flip it to '0' (cost = cost_to_0)
    if root_val == '0':
        print(cost_to_1)
    else:
        print(cost_to_0)

if __name__ == '__main__':
    solve()