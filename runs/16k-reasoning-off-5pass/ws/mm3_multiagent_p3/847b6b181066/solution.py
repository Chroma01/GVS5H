import sys

def solve():
    input = sys.stdin.readline
    N, R, C = map(int, input().split())
    S = input().strip()
    
    # Wind direction vectors
    dirs = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    
    # Current position (prefix_wind)
    cr, cc = 0, 0
    
    # Set of prefix positions for which a smoke puff exists
    seen = {(0, 0)}
    
    result = []
    
    for t in range(N):
        # Apply wind t+1
        dr, dc = dirs[S[t]]
        cr += dr
        cc += dc
        
        # Check if target (R, C) is occupied: target_prefix = (cr - R, cc - C)
        if (cr - R, cc - C) in seen:
            result.append('1')
        else:
            result.append('0')
        
        # Check if campfire is empty -> generate new smoke
        if (cr, cc) not in seen:
            seen.add((cr, cc))
    
    print(''.join(result))

solve()