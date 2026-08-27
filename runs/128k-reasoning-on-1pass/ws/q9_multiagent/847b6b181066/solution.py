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
    
    # Set to store visited positions of the original smoke particle
    # Initially at (0,0) at t=0
    visited = set()
    visited.add((0, 0))
    
    # Current position of the original smoke particle
    curr_r, curr_c = 0, 0
    
    # List to store the result characters
    ans = []
    
    # Simulate for t = 1 to N
    for char in S:
        # Update current position based on wind direction
        if char == 'N':
            curr_r -= 1
        elif char == 'W':
            curr_c -= 1
        elif char == 'S':
            curr_r += 1
        elif char == 'E':
            curr_c += 1
        
        # Check if smoke exists at (R, C) at time t+0.5
        # Smoke exists if there was a birth at time b < t such that
        # position of particle born at b at time t is (R, C).
        # Position of particle born at b at time t is D_t - D_b.
        # So we need D_t - D_b = (R, C) => D_b = D_t - (R, C).
        # We need to check if D_t - (R, C) is in the set of positions visited by original particle.
        # Since we only care about b < t, and D_b must be a "first visit" position for b to be a birth time,
        # checking if D_t - (R, C) is in the set of unique positions visited so far is sufficient.
        
        target_r = curr_r - R
        target_c = curr_c - C
        
        if (target_r, target_c) in visited:
            ans.append('1')
        else:
            ans.append('0')
            
        # Update visited set with current position if it's new
        # This corresponds to checking if smoke exists at (0,0) at time t.
        # If not, new smoke is generated, which means D_t is a new birth position.
        if (curr_r, curr_c) not in visited:
            visited.add((curr_r, curr_c))
            
    print("".join(ans))

if __name__ == '__main__':
    solve()