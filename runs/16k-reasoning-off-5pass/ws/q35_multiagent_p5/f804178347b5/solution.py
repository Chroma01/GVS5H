import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    A_str = input_data[1]
    
    # Length of the string is 3^N
    # Initialize costs for leaves
    # costs[i] = (cost0, cost1) for the i-th node at the current level
    # cost0: min changes to make this node output 0
    # cost1: min changes to make this node output 1
    costs = []
    for bit in A_str:
        if bit == '0':
            costs.append((0, 1))
        else:
            costs.append((1, 0))
            
    # Process level by level from bottom to top
    # There are N levels of internal nodes to process
    for level in range(N):
        new_costs = []
        # Iterate through the current costs list in groups of 3
        for i in range(0, len(costs), 3):
            c0_1, c1_1 = costs[i]
            c0_2, c1_2 = costs[i+1]
            c0_3, c1_3 = costs[i+2]
            
            # Compute cost0 for the parent: need at least two children to be 0
            # Option 1: children 1 and 2 are 0, child 3 is anything (min cost to be either 0 or 1)
            opt1 = c0_1 + c0_2 + min(c0_3, c1_3)
            # Option 2: children 1 and 3 are 0, child 2 is anything
            opt2 = c0_1 + c0_3 + min(c0_2, c1_2)
            # Option 3: children 2 and 3 are 0, child 1 is anything
            opt3 = c0_2 + c0_3 + min(c0_1, c1_1)
            
            cost0 = min(opt1, opt2, opt3)
            
            # Compute cost1 for the parent: need at least two children to be 1
            # Option 1: children 1 and 2 are 1, child 3 is anything
            opt1 = c1_1 + c1_2 + min(c0_3, c1_3)
            # Option 2: children 1 and 3 are 1, child 2 is anything
            opt2 = c1_1 + c1_3 + min(c0_2, c1_2)
            # Option 3: children 2 and 3 are 1, child 1 is anything
            opt3 = c1_2 + c1_3 + min(c0_1, c1_1)
            
            cost1 = min(opt1, opt2, opt3)
            
            new_costs.append((cost0, cost1))
            
        costs = new_costs
        
    # Now costs has only one element: the root's (cost0, cost1)
    root_cost0, root_cost1 = costs[0]
    
    # Determine the original value of the root by simulating the majority operation
    current = list(A_str)
    for _ in range(N):
        new_current = []
        for i in range(0, len(current), 3):
            group = current[i:i+3]
            # Majority vote: if at least two are '1', result is '1', else '0'
            if group.count('1') > 1:
                new_current.append('1')
            else:
                new_current.append('0')
        current = new_current
        
    original_root = current[0]
    
    if original_root == '0':
        # We need to change it to 1, so answer is root_cost1
        print(root_cost1)
    else:
        # We need to change it to 0, so answer is root_cost0
        print(root_cost0)

if __name__ == '__main__':
    solve()