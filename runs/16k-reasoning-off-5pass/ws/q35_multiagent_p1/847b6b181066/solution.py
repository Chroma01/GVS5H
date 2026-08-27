import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse N, R, C
    N = int(input_data[0])
    R = int(input_data[1])
    C = int(input_data[2])
    
    # Parse S
    S = input_data[3]
    
    # Direction mappings
    # N: r-1, c
    # S: r+1, c
    # W: r, c-1
    # E: r, c+1
    dr = {'N': -1, 'S': 1, 'W': 0, 'E': 0}
    dc = {'N': 0, 'S': 0, 'W': -1, 'E': 1}
    
    # Current prefix sum position (r, c)
    # P_0 = (0, 0)
    curr_r = 0
    curr_c = 0
    
    # Set of seen prefix positions
    seen_positions = set()
    seen_positions.add((0, 0))
    
    result = []
    
    # Target displacement we need to have occurred from some previous P_k to P_t
    # P_t - P_k = (R, C)  =>  P_k = P_t - (R, C)
    target_dr = R
    target_dc = C
    
    for i in range(N):
        char = S[i]
        
        # Update current prefix position P_{i+1}
        curr_r += dr[char]
        curr_c += dc[char]
        
        # We are at time t = i+1.
        # We need to check if there exists k in 0..t such that P_k = P_t - (R, C).
        # Note: P_t is the current (curr_r, curr_c).
        # We need to check if (curr_r - R, curr_c - C) is in seen_positions.
        # But wait, seen_positions currently contains P_0 ... P_i.
        # For time t=i+1, the possible k values are 0, 1, ..., i+1.
        # So we need to include P_{i+1} in the set before checking?
        # Actually, if k = i+1, then P_k = P_t, so we check if P_t - (R,C) == P_t => (R,C) == (0,0).
        # Since (R,C) != (0,0), k=i+1 never contributes.
        # So we only need to check against P_0 ... P_i.
        # However, for the NEXT step, we will need P_{i+1}.
        
        target_r = curr_r - target_dr
        target_c = curr_c - target_dc
        
        if (target_r, target_c) in seen_positions:
            result.append('1')
        else:
            result.append('0')
            
        # Add current position P_{i+1} to seen set for future checks
        seen_positions.add((curr_r, curr_c))
        
    print("".join(result))

if __name__ == '__main__':
    solve()