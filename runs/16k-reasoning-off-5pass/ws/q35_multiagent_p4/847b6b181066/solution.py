import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    R = int(input_data[1])
    C = int(input_data[2])
    S = input_data[3]

    # Map directions to displacement vectors
    # N: r-1, S: r+1, W: c-1, E: c+1
    dir_map = {
        'N': (-1, 0),
        'S': (1, 0),
        'W': (0, -1),
        'E': (0, 1)
    }

    # Current cumulative displacement P_t
    # P_0 = (0, 0)
    curr_r, curr_c = 0, 0
    
    # Set of all P_k for k in [0, t-1]
    # Initially contains P_0
    seen_positions = set()
    seen_positions.add((0, 0))
    
    result = []
    
    for i in range(N):
        # The t-th character corresponds to step t = i+1
        # Wind direction for this step
        wind = S[i]
        dr, dc = dir_map[wind]
        
        # Update cumulative displacement to P_t
        curr_r += dr
        curr_c += dc
        
        # We want to check if there exists k in [0, t] such that P_k = P_t - (R, C)
        # Note: P_t is now computed. The set 'seen_positions' contains P_0, ..., P_{t-1}.
        # We need to check if P_t - (R, C) is in seen_positions.
        # If it is, then there exists a k < t such that P_k = P_t - (R, C).
        # This means a particle generated at time k (or initial at k=0) is at (R,C) at time t.
        
        target_r = curr_r - R
        target_c = curr_c - C
        
        if (target_r, target_c) in seen_positions:
            result.append('1')
        else:
            result.append('0')
            
        # Add P_t to the set for future steps
        seen_positions.add((curr_r, curr_c))
        
    print("".join(result))

if __name__ == '__main__':
    solve()