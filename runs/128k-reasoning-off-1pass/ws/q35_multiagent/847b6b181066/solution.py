import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    R = int(input_data[1])
    C = int(input_data[2])
    S = input_data[3]
    
    # Current cumulative displacement from (0,0)
    # D_t is the position after t wind blows, starting from (0,0)
    curr_r, curr_c = 0, 0
    
    # Set of all D_k for k < t (initially k=0, D_0 = (0,0))
    seen = set()
    seen.add((0, 0))
    
    result = []
    
    # Directions mapping
    # N: r-1, S: r+1, W: c-1, E: c+1
    dirs = {
        'N': (-1, 0),
        'S': (1, 0),
        'W': (0, -1),
        'E': (0, 1)
    }
    
    for i in range(N):
        char = S[i]
        dr, dc = dirs[char]
        curr_r += dr
        curr_c += dc
        
        # We are at time t = i + 1
        # We want to know if there exists k < t such that D_k = D_t - (R, C)
        target_r = curr_r - R
        target_c = curr_c - C
        
        if (target_r, target_c) in seen:
            result.append('1')
        else:
            result.append('0')
            
        # Add current D_t to seen for future steps
        seen.add((curr_r, curr_c))
        
    print("".join(result))

if __name__ == '__main__':
    solve()