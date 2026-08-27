import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Dictionary to store [L, R] for each column
    # L is the minimum number of black cells (from 'B' constraints)
    # R is the maximum number of black cells (from 'W' constraints)
    constraints = {}
    
    for _ in range(M):
        try:
            x = int(next(iterator))
            y = int(next(iterator))
            c = next(iterator)
        except StopIteration:
            break
        
        if y not in constraints:
            constraints[y] = [0, N]
        
        if c == 'B':
            # Black cell at row x means K_y >= x
            constraints[y][0] = max(constraints[y][0], x)
        else:
            # White cell at row x means K_y <= x - 1
            constraints[y][1] = min(constraints[y][1], x - 1)
    
    # Check for local contradictions within each column
    for y in constraints:
        if constraints[y][0] > constraints[y][1]:
            print("No")
            return

    # Check the global non-increasing condition: K_1 >= K_2 >= ... >= K_N
    # A non-increasing sequence K exists satisfying L_c <= K_c <= R_c 
    # if and only if for all c, L_c <= min(R_1, R_2, ..., R_c).
    # We only need to check this for columns with constraints.
    # Unconstrained columns have L=0, R=N, so L <= min_R is always true.
    
    sorted_ys = sorted(constraints.keys())
    min_R = N  # Initial min_R for columns before the first constrained one
    
    for y in sorted_ys:
        min_R = min(min_R, constraints[y][1])
        if constraints[y][0] > min_R:
            print("No")
            return
            
    print("Yes")

if __name__ == '__main__':
    solve()