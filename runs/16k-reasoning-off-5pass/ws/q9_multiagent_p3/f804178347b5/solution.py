import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    a_str = input_data[1]
    
    # Current values of the nodes at the current level (initially leaves)
    # We use integers 0 and 1
    values = [int(c) for c in a_str]
    
    # Costs to flip the value of each node at the current level
    # Initially, for leaves, the cost to flip is 1
    costs = [1] * len(values)
    
    # Length of the current level
    current_len = len(values)
    
    # Iterate N times to move from leaves up to the root
    for _ in range(n):
        next_len = current_len // 3
        next_values = [0] * next_len
        next_costs = [0] * next_len
        
        # Process each node in the next level
        for i in range(next_len):
            # Indices of children in the current level
            idx1 = i * 3
            idx2 = i * 3 + 1
            idx3 = i * 3 + 2
            
            v1 = values[idx1]
            v2 = values[idx2]
            v3 = values[idx3]
            
            c1 = costs[idx1]
            c2 = costs[idx2]
            c3 = costs[idx3]
            
            # Determine current majority value
            # Since there are 3 values, majority is the one appearing >= 2 times
            if v1 == v2 or v1 == v3:
                current_val = v1
            elif v2 == v3:
                current_val = v2
            else:
                current_val = v3
            
            # Determine cost to flip the current_val
            # We need to change the majority to (1 - current_val)
            
            # Collect costs of children that have the current majority value
            majority_costs = []
            if v1 == current_val:
                majority_costs.append(c1)
            if v2 == current_val:
                majority_costs.append(c2)
            if v3 == current_val:
                majority_costs.append(c3)
            
            # There are either 2 or 3 children with the current majority value
            if len(majority_costs) == 3:
                # Case: All three are current_val. 
                # To flip majority, we need to flip at least two children.
                # We pick the two with the smallest costs.
                majority_costs.sort()
                next_costs[i] = majority_costs[0] + majority_costs[1]
            else:
                # Case: Two are current_val, one is different.
                # To flip majority, we need to flip one of the current_val children.
                # We pick the one with the smallest cost.
                next_costs[i] = min(majority_costs)
            
            next_values[i] = current_val
        
        # Update state for next iteration
        values = next_values
        costs = next_costs
        current_len = next_len
        
    # The answer is the cost to flip the root value
    print(costs[0])

if __name__ == '__main__':
    solve()