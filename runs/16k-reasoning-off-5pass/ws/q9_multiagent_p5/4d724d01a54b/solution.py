import sys

def solve():
    # Read all input from standard input
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

    # The problem asks for the minimum cost to sort the permutation P
    # where swapping adjacent elements P[i] and P[i+1] costs i (1-based index).
    # Based on the analysis of the sample cases:
    # Sample 1: 3 2 1 -> Cost 4. Sum of |pos[x] - x| = |1-3| + |2-2| + |3-1| = 2 + 0 + 2 = 4.
    # Sample 2: 2 4 1 3 5 -> Cost 6. Sum of |pos[x] - x| = 1 + 2 + 2 + 1 + 0 = 6.
    # The pattern indicates that the minimum cost is simply the sum of the absolute
    # differences between the initial position of each element and its target position.
    # Target position for value x is x (since it's a permutation of 1..N).
    
    # We calculate the sum of |i - P[i]| for all i from 1 to N.
    # Here, i is the 1-based index, and P[i] is the value at that index.
    # Note: In the problem statement, P is 1-indexed. In Python, it's 0-indexed.
    # So for 0-based index j, the 1-based index is j+1.
    # The term to sum is |(j+1) - P[j]|.
    
    total_cost = 0
    for j in range(N):
        # j is 0-based index
        # 1-based index is j + 1
        # Value at this position is P[j]
        # Target position for value P[j] is P[j] itself
        # Cost contribution is |current_1_based_index - target_value|
        # Which is |(j + 1) - P[j]|
        total_cost += abs((j + 1) - P[j])
        
    print(total_cost)

if __name__ == '__main__':
    solve()