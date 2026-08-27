import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    R = int(input_data[1])
    C = int(input_data[2])
    S = input_data[3]

    # We need to determine if smoke exists at (R, C) at time t + 0.5 for each t from 1 to N.
    # 
    # Logic derivation:
    # Let D_t be the cumulative displacement vector after t steps of wind.
    # D_0 = (0, 0)
    # D_t = D_{t-1} + displacement(S[t-1])
    #
    # Smoke generated at time k (where 0 <= k < t) at position (0,0) will have moved
    # according to the wind sequence from step k+1 to t.
    # The number of steps it has moved is t - k.
    # Its position at time t is: (0,0) + (D_t - D_k).
    #
    # We want to check if there exists any k in {0, ..., t-1} such that:
    # (0,0) + (D_t - D_k) == (R, C)
    # => D_k == D_t - (R, C)
    #
    # So for each t, we calculate target = D_t - (R, C) and check if target exists
    # in the set of previous displacements {D_0, D_1, ..., D_{t-1}}.
    # If it exists, output '1', else '0'.
    # Then we add D_t to the set for the next iteration.

    # Precompute displacements or compute on the fly.
    # Since we need D_t for each step, we can maintain the current displacement.
    
    curr_r, curr_c = 0, 0
    # Set to store {D_0, D_1, ..., D_{t-1}}
    # Initially contains D_0 = (0, 0)
    seen_displacements = set()
    seen_displacements.add((0, 0))
    
    result = []
    
    # Directions mapping
    # N: (-1, 0), W: (0, -1), S: (1, 0), E: (0, 1)
    # Note: Problem says N moves (r,c) to (r-1, c). So r decreases.
    # W moves (r,c) to (r, c-1). So c decreases.
    # S moves (r,c) to (r+1, c). So r increases.
    # E moves (r,c) to (r, c+1). So c increases.
    
    for t in range(N):
        char = S[t]
        
        # Update current displacement D_{t+1} based on wind S[t]
        if char == 'N':
            curr_r -= 1
        elif char == 'W':
            curr_c -= 1
        elif char == 'S':
            curr_r += 1
        elif char == 'E':
            curr_c += 1
            
        # Current displacement is D_{t+1} (since t is 0-indexed loop, this is step t+1)
        # We are checking for time (t+1) + 0.5
        target_r = curr_r - R
        target_c = curr_c - C
        
        if (target_r, target_c) in seen_displacements:
            result.append('1')
        else:
            result.append('0')
            
        # Add current displacement to the set for future checks
        seen_displacements.add((curr_r, curr_c))
        
    print("".join(result))

if __name__ == '__main__':
    solve()