import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    # P is 1-indexed in the problem statement, but we can work with 0-indexed or 1-indexed consistently.
    # The formula is sum(|initial_position[v] - target_position[v]|) for v in 1..N.
    # If we use 1-indexed positions:
    # Value v should be at position v.
    # We are given P_1, P_2, ..., P_N.
    # P_i is the value at position i.
    # So for value v, its initial position is the index i such that P_i = v.
    
    # Let's create an array where pos[v] = initial position of value v (1-indexed).
    # input_data[1] to input_data[N] are P_1 to P_N.
    
    p = []
    for i in range(1, n + 1):
        p.append(int(input_data[i]))
        
    # pos[v] stores the 1-indexed position of value v.
    # Since values are 1 to N, we can use a list of size N+1.
    pos = [0] * (n + 1)
    for idx, val in enumerate(p):
        # idx is 0-indexed, so position is idx + 1
        pos[val] = idx + 1
        
    total_cost = 0
    for v in range(1, n + 1):
        # Target position for value v is v (1-indexed)
        # Initial position is pos[v]
        total_cost += abs(pos[v] - v)
        
    print(total_cost)

if __name__ == '__main__':
    solve()