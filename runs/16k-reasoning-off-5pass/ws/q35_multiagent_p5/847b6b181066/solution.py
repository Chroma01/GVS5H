import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    R = int(input_data[1])
    C = int(input_data[2])
    S = input_data[3]
    
    # Current displacement from origin (0,0) after t moves
    dr = 0
    dc = 0
    
    # Set of seen displacements (dr[k], dc[k]) for k from 0 to t-1
    # Initially, at t=0, displacement is (0,0)
    seen = set()
    seen.add((0, 0))
    
    result = []
    
    # Direction mappings
    # N: r-1, S: r+1, W: c-1, E: c+1
    moves = {
        'N': (-1, 0),
        'S': (1, 0),
        'W': (0, -1),
        'E': (0, 1)
    }
    
    for i in range(N):
        char = S[i]
        d_r, d_c = moves[char]
        dr += d_r
        dc += d_c
        
        # We want to know if there exists k < t (where t = i+1)
        # such that (dr[k], dc[k]) == (dr - R, dc - C)
        target_dr = dr - R
        target_dc = dc - C
        
        if (target_dr, target_dc) in seen:
            result.append('1')
        else:
            result.append('0')
            
        # Add current displacement to seen set for future checks
        seen.add((dr, dc))
        
    print("".join(result))

if __name__ == '__main__':
    solve()