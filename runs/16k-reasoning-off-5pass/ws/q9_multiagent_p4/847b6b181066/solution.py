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

    # We need to track the set of occupied cells.
    # Instead of storing absolute coordinates which shift every time,
    # we store relative coordinates with respect to the current "wind origin".
    # Let 'offset' be the cumulative displacement of the wind from t=1 to current t.
    # If a smoke particle is at absolute position (r, c), we store (r - offset_r, c - offset_c).
    # When wind blows with vector (dr, dc), the absolute position of all particles shifts by (dr, dc).
    # In relative terms, the stored coordinate (r_rel, c_rel) becomes:
    # (r + dr) - (offset_r + dr) = r_rel
    # So the relative coordinates of existing particles do NOT change when wind blows.
    # The only change is that the "origin" (0,0) in absolute coordinates moves to (-offset_r, -offset_c) in relative coordinates.
    # If the absolute (0,0) is empty, new smoke is generated there.
    # In relative terms, this new smoke is at (0 - offset_r, 0 - offset_c) = (-offset_r, -offset_c).
    
    # Current cumulative wind displacement (dr, dc)
    offset_r = 0
    offset_c = 0
    
    # Set to store relative coordinates of smoke particles
    smoke_set = set()
    
    # Initial state at t=0: smoke at (0,0).
    # Relative coordinate: (0, 0) - (0, 0) = (0, 0)
    smoke_set.add((0, 0))
    
    result = []
    
    # Directions mapping
    # N: (-1, 0), W: (0, -1), S: (1, 0), E: (0, 1)
    dir_map = {
        'N': (-1, 0),
        'W': (0, -1),
        'S': (1, 0),
        'E': (0, 1)
    }
    
    for char in S:
        dr, dc = dir_map[char]
        
        # Update the global offset
        offset_r += dr
        offset_c += dc
        
        # Check if absolute (0,0) is occupied.
        # In relative coordinates, absolute (0,0) corresponds to (-offset_r, -offset_c).
        # If it is NOT occupied, add new smoke at absolute (0,0).
        # Relative coordinate of new smoke: (0 - offset_r, 0 - offset_c)
        new_smoke_rel = (-offset_r, -offset_c)
        
        if new_smoke_rel not in smoke_set:
            smoke_set.add(new_smoke_rel)
        
        # Check if target (R, C) is occupied.
        # Absolute (R, C) corresponds to (R - offset_r, C - offset_c) in relative coordinates.
        target_rel = (R - offset_r, C - offset_c)
        
        if target_rel in smoke_set:
            result.append('1')
        else:
            result.append('0')
            
    print("".join(result))

if __name__ == '__main__':
    solve()