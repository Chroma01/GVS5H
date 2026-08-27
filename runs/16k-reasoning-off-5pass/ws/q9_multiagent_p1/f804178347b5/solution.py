import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    A = input_data[1]
    
    # Length of the string is 3^N
    L = 3 ** N
    
    # We will process the tree level by level from bottom (leaves) to top (root).
    # Level N corresponds to the leaves (original string A).
    # Level 0 corresponds to the root.
    
    # current_vals stores the bit values at the current level.
    # current_costs stores the minimum cost to flip the value of each node at the current level.
    
    current_vals = list(A)
    # Cost to flip any leaf is 1.
    current_costs = [1] * len(current_vals)
    
    # Iterate N times to go from level N down to level 0 (root)
    # In each iteration, we reduce the size by factor of 3.
    for _ in range(N):
        next_vals = []
        next_costs = []
        
        num_nodes = len(current_vals)
        num_parents = num_nodes // 3
        
        for i in range(num_parents):
            # Indices of children in the current level
            idx1 = 3 * i
            idx2 = 3 * i + 1
            idx3 = 3 * i + 2
            
            val1 = current_vals[idx1]
            val2 = current_vals[idx2]
            val3 = current_vals[idx3]
            
            # Determine majority value for the parent
            # Count occurrences
            counts = {val1: 1, val2: 1, val3: 1}
            # Identify the value that appears most frequently
            majority = None
            for v in [val1, val2, val3]:
                if counts[v] == 2:
                    majority = v
                    break
            
            # Calculate cost to flip the parent's value
            # Logic:
            # 1. If all 3 children are same (v, v, v):
            #    To flip the majority (v) to (not v), we need to flip at least 2 children.
            #    Since all children have value v, cost = cost(v) + cost(v) = 2 * current_costs[idx1]
            # 2. If children are mixed (v, v, !v):
            #    The majority is v. To flip the majority to (!v), we need to flip one of the v's to !v.
            #    Flipping the !v child would result in (v, v, v), which still has majority v.
            #    So we must flip a child with value v. Cost = current_costs[child_index_with_value_v].
            
            if val1 == val2 == val3:
                cost = 2 * current_costs[idx1]
            else:
                # Mixed case: find the child with the majority value
                if val1 == val2:
                    cost = current_costs[idx1]
                elif val1 == val3:
                    cost = current_costs[idx1]
                else:
                    cost = current_costs[idx2]
            
            next_vals.append(majority)
            next_costs.append(cost)
            
        current_vals = next_vals
        current_costs = next_costs
        
    # After N iterations, current_costs[0] is the answer for the root
    print(current_costs[0])

if __name__ == '__main__':
    solve()