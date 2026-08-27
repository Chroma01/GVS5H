import sys

def solve():
    # Read all input from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    N = int(input_data[0])
    R = int(input_data[1])
    C = int(input_data[2])
    S = input_data[3]
    
    # Current position of the reference smoke particle (initially at (0,0))
    cur_r, cur_c = 0, 0
    
    # Set to store all positions visited by the reference particle
    # Initially contains the starting position
    visited = {(0, 0)}
    
    res = []
    
    for char in S:
        # Update reference particle position based on wind direction
        if char == 'N':
            cur_r -= 1
        elif char == 'W':
            cur_c -= 1
        elif char == 'S':
            cur_r += 1
        elif char == 'E':
            cur_c += 1
            
        # Smoke exists at (R, C) at time t+0.5 if and only if
        # there exists some k <= t such that P_t - P_k = (R, C).
        # This is equivalent to checking if P_t - (R, C) is in {P_0, ..., P_t}.
        # Since (R, C) != (0, 0), we only need to check previous positions.
        if (cur_r - R, cur_c - C) in visited:
            res.append('1')
        else:
            res.append('0')
            
        # Add current position to visited set for future checks
        visited.add((cur_r, cur_c))
        
    # Print the result string
    print("".join(res))

if __name__ == '__main__':
    solve()