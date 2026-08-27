import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        p = []
        for _ in range(n):
            p.append(int(next(iterator)))
    except StopIteration:
        return

    # The problem asks for the minimum cost to sort the permutation P.
    # Swapping P[i] and P[i+1] (0-indexed i) costs i+1.
    # It turns out that for this specific cost function, the minimum total cost
    # is exactly the sum of absolute differences between the value at each position
    # and the position itself (1-based).
    # Formula: sum(|P[i] - (i + 1)|) for i from 0 to N-1.
    
    total_cost = 0
    for i in range(n):
        # i is 0-based index, so the 1-based index is i + 1
        val = p[i]
        target_pos = i + 1
        total_cost += abs(val - target_pos)
        
    print(total_cost)

if __name__ == '__main__':
    solve()