import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse inputs
    N = int(input_data[0])
    R = int(input_data[1])
    C = int(input_data[2])
    S = input_data[3]

    # Set to store the "base" coordinates of all smoke particles.
    # A particle with base coordinate (br, bc) will be at physical position
    # (br + dx, bc + dy) where (dx, dy) is the current cumulative wind offset.
    bases = set()
    
    # Initially, smoke is at (0,0) at t=0.
    # Its base coordinate is (0,0) because the initial offset is (0,0).
    bases.add((0, 0))

    # Current cumulative wind displacement (dx, dy)
    dx, dy = 0, 0
    
    # Directions mapping
    # N: (r-1, c) -> (-1, 0)
    # W: (r, c-1) -> (0, -1)
    # S: (r+1, c) -> (1, 0)
    # E: (r, c+1) -> (0, 1)
    dir_map = {
        'N': (-1, 0),
        'W': (0, -1),
        'S': (1, 0),
        'E': (0, 1)
    }

    result = []

    for char in S:
        dr, dc = dir_map[char]
        dx += dr
        dy += dc
        
        # Check if smoke exists at (R, C) at this time step (t+0.5)
        # Physical position of a base (br, bc) is (br + dx, bc + dy)
        # We need (br + dx == R) and (bc + dy == C)
        # So we check if (R - dx, C - dy) is in bases
        target_base = (R - dx, C - dy)
        if target_base in bases:
            result.append('1')
        else:
            result.append('0')
            
        # Regeneration logic:
        # If there is no smoke in cell (0,0), new smoke is generated.
        # Check if (0,0) is occupied physically.
        # Physical (0,0) corresponds to base coordinate (0 - dx, 0 - dy) = (-dx, -dy)
        if (-dx, -dy) not in bases:
            bases.add((-dx, -dy))

    print("".join(result))

if __name__ == '__main__':
    solve()