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

    # Target position to check
    target_r, target_c = R, C
    
    # We need to check if smoke exists at (R, C) at time t+0.5 for each t from 1 to N.
    # 
    # Logic Analysis:
    # Let T_t be the cumulative displacement vector after t wind blows. T_0 = (0, 0).
    # A smoke particle generated at time k (appearing at (0,0) at time k+0.5) 
    # will be at position T_t - T_k at time t+0.5.
    #
    # A new particle is generated at time k (for the next step) IF AND ONLY IF
    # there is NO smoke at (0,0) at time k+0.5.
    # Smoke is at (0,0) at time k+0.5 if there exists some j < k such that a particle 
    # generated at j lands on (0,0) at step k.
    # Position of particle generated at j at time k is T_k - T_j.
    # So, smoke is at (0,0) at time k+0.5 iff exists j < k such that T_k - T_j = (0,0) => T_k = T_j.
    #
    # Therefore, a new particle is generated at time k (available for step k+1) if and only if
    # T_k has NOT appeared in the sequence T_0, T_1, ..., T_{k-1}.
    # Let's call such a T_k a "unique" position.
    #
    # The set of occupied cells at time t+0.5 is:
    # { T_t - T_k | 0 <= k < t AND T_k is unique }
    #
    # We need to check if (R, C) is in this set.
    # (R, C) is in the set iff exists k < t such that T_k is unique AND T_t - T_k = (R, C).
    # This is equivalent to: exists k < t such that T_k is unique AND T_k = T_t - (R, C).
    #
    # Algorithm:
    # 1. Maintain a set `seen` of positions T_k encountered so far.
    # 2. Maintain a set `unique_positions` of positions T_k that are unique (i.e., T_k not in seen before).
    # 3. Iterate t from 1 to N:
    #    a. Calculate T_t (update current position).
    #    b. Check if T_t is in `seen`.
    #       - If no: Add T_t to `seen` and `unique_positions`.
    #       - If yes: Do nothing (T_t is not unique).
    #    c. Check if (T_t - (R, C)) is in `unique_positions`.
    #       - If yes, append '1' to result.
    #       - Else, append '0'.
    
    seen = set()
    unique_positions = set()
    
    curr_r, curr_c = 0, 0
    # Initial state at t=0
    seen.add((curr_r, curr_c))
    unique_positions.add((curr_r, curr_c))
    
    result = []
    
    # Directions mapping based on problem statement:
    # N: (r, c) -> (r-1, c)
    # W: (r, c) -> (r, c-1)
    # S: (r, c) -> (r+1, c)
    # E: (r, c) -> (r, c+1)
    dir_map = {
        'N': (-1, 0),
        'W': (0, -1),
        'S': (1, 0),
        'E': (0, 1)
    }
    
    for char in S:
        dr, dc = dir_map[char]
        curr_r += dr
        curr_c += dc
        
        # Current position is T_t
        current_pos = (curr_r, curr_c)
        
        # Check if this position is new (unique)
        if current_pos not in seen:
            seen.add(current_pos)
            unique_positions.add(current_pos)
        
        # Check if smoke is at (R, C)
        # Condition: exists k < t such that T_k is unique AND T_k = T_t - (R, C)
        # So we check if (curr_r - R, curr_c - C) is in unique_positions
        needed_pos = (curr_r - R, curr_c - C)
        
        if needed_pos in unique_positions:
            result.append('1')
        else:
            result.append('0')
            
    print("".join(result))

if __name__ == '__main__':
    solve()