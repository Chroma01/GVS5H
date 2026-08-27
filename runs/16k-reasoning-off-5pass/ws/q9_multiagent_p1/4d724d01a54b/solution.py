import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from standard input efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n_str = next(iterator)
        N = int(n_str)
        
        P = []
        for _ in range(N):
            P.append(int(next(iterator)))
    except StopIteration:
        return

    # The problem asks for the minimum cost to sort a permutation P where swapping 
    # adjacent elements P[i] and P[i+1] (0-indexed) costs i+1 (since the problem uses 1-based indexing for cost).
    # Specifically, swapping the element at index i (1-based) and i+1 costs i.
    # In 0-based indexing, swapping index i and i+1 costs i+1.
    
    # Analysis of samples reveals that the minimum total cost is equal to the sum of 
    # absolute displacements of each element from its target position.
    # Target position for value x is x (1-based) or x-1 (0-based).
    # Cost = sum(|pos[x] - target[x]|) for all x in 1..N.
    
    # We need to find the initial position of each value x.
    # Since values are a permutation of 1 to N, we can use an array 'pos' where pos[x] stores the index of x.
    
    pos = [0] * (N + 1)
    for index, value in enumerate(P):
        pos[value] = index
    
    total_cost = 0
    for x in range(1, N + 1):
        current_pos = pos[x]      # 0-based index where value x is currently located
        target_pos = x - 1        # 0-based index where value x should be located
        total_cost += abs(current_pos - target_pos)
        
    print(total_cost)

if __name__ == '__main__':
    solve()