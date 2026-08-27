import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    R = int(input_data[1])
    C = int(input_data[2])
    S = input_data[3]
    
    # Track the position of the original smoke particle starting at (0,0) at time 0
    # P_t is the position after t wind blows
    curr_r = 0
    curr_c = 0
    
    # Set of all positions P_k for k from 0 to t-1
    visited = set()
    visited.add((0, 0))
    
    result = []
    
    # Direction mappings
    # N: r-1, S: r+1, W: c-1, E: c+1
    dr = {'N': -1, 'S': 1, 'W': 0, 'E': 0}
    dc = {'N': 0, 'S': 0, 'W': -1, 'E': 1}
    
    for t in range(1, N + 1):
        wind = S[t-1]
        
        # Update current position P_t
        curr_r += dr[wind]
        curr_c += dc[wind]
        
        # We want to check if there exists k in [0, t-1] such that P_k = P_t - (R, C)
        target_r = curr_r - R
        target_c = curr_c - C
        
        if (target_r, target_c) in visited:
            result.append('1')
        else:
            result.append('0')
            
        # Add P_t to visited for future steps
        visited.add((curr_r, curr_c))
        
    print("".join(result))

if __name__ == '__main__':
    solve()