import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    A_str = input_data[1]
    
    # Length of the string is 3^N
    L = 3 ** N
    
    # Initialize DP arrays for the leaves (level 0)
    # current_dp0[i] = min cost to make leaf i -> 0
    # current_dp1[i] = min cost to make leaf i -> 1
    current_dp0 = [0] * L
    current_dp1 = [0] * L
    
    for i in range(L):
        if A_str[i] == '0':
            current_dp0[i] = 0
            current_dp1[i] = 1
        else:
            current_dp0[i] = 1
            current_dp1[i] = 0
            
    # Simulate the process to find the initial root value
    current_vals = [int(c) for c in A_str]
    
    for level in range(N):
        next_vals = []
        size = len(current_vals)
        for i in range(0, size, 3):
            v1 = current_vals[i]
            v2 = current_vals[i+1]
            v3 = current_vals[i+2]
            # Majority vote
            if v1 == v2 or v1 == v3 or v2 == v3:
                next_vals.append(v1)
            else:
                next_vals.append(v2)
        current_vals = next_vals
        
    initial_root = current_vals[0]
    
    # Compute DP bottom-up to find min cost to flip the root
    for level in range(N):
        next_dp0 = [0] * (len(current_dp0) // 3)
        next_dp1 = [0] * (len(current_dp0) // 3)
        
        for i in range(0, len(current_dp0), 3):
            c0 = current_dp0[i]
            c1 = current_dp0[i+1]
            c2 = current_dp0[i+2]
            
            d0 = current_dp1[i]
            d1 = current_dp1[i+1]
            d2 = current_dp1[i+2]
            
            # To make this node 0, at least two children must be 0.
            # Combinations: (0,0,0), (0,0,1), (0,1,0), (1,0,0)
            val1 = c0 + c1 + c2
            val2 = c0 + c1 + d2
            val3 = c0 + d1 + c2
            val4 = d0 + c1 + c2
            next_dp0[i//3] = min(val1, val2, val3, val4)
            
            # To make this node 1, at least two children must be 1.
            # Combinations: (1,1,1), (1,1,0), (1,0,1), (0,1,1)
            val5 = d0 + d1 + d2
            val6 = d0 + d1 + c2
            val7 = d0 + c1 + d2
            val8 = c0 + d1 + d2
            next_dp1[i//3] = min(val5, val6, val7, val8)
            
        current_dp0 = next_dp0
        current_dp1 = next_dp1
        
    # Determine the answer based on the initial root value
    if initial_root == 1:
        print(current_dp0[0])
    else:
        print(current_dp1[0])

if __name__ == '__main__':
    solve()