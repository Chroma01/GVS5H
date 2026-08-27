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

    # Directions mapping
    # N: (r-1, c), W: (r, c-1), S: (r+1, c), E: (r, c+1)
    moves = {
        'N': (-1, 0),
        'W': (0, -1),
        'S': (1, 0),
        'E': (0, 1)
    }

    # Precompute prefix sums P
    # P[i] is the position of the smoke generated at t=0 after i wind steps.
    # P[0] = (0, 0)
    # P[i] = P[i-1] + move(S[i-1])
    
    P = [(0, 0)] * (N + 1)
    curr_r, curr_c = 0, 0
    for i in range(N):
        dr, dc = moves[S[i]]
        curr_r += dr
        curr_c += dc
        P[i+1] = (curr_r, curr_c)

    # Logic:
    # At time t (after t wind steps), the set of occupied cells is:
    # { P[t] - P[j] | -1 <= j <= t-1 AND (j == -1 OR P[j+1] != (0,0)) }
    # We need to check if (R, C) is in this set.
    # This is equivalent to checking if P[t] - (R, C) is in { P[j] | valid j }.
    
    # valid_offsets stores P[j] for valid j < current_t
    # j = -1 corresponds to P[-1] = (0,0) which is always valid.
    valid_offsets = set()
    valid_offsets.add((0, 0)) 
    
    result = []
    
    for t in range(1, N + 1):
        # Check existence at time t
        # Target offset needed: P[t] - (R, C)
        target = (P[t][0] - R, P[t][1] - C)
        
        if target in valid_offsets:
            result.append('1')
        else:
            result.append('0')
        
        # Prepare valid_offsets for the next step (t+1)
        # We need to add P[t] to the set if it is a valid offset for step t+1.
        # P[t] is a valid offset for step t+1 if P[t+1] != (0,0).
        # Note: P[t] corresponds to j=t. The condition for j is P[j+1] != (0,0).
        if t < N:
            if P[t+1] != (0, 0):
                valid_offsets.add(P[t])
    
    print("".join(result))

if __name__ == '__main__':
    solve()