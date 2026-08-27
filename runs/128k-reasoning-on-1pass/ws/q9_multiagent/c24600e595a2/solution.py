import sys

def solve():
    # Read all input from standard input efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        # Read N
        n_str = next(iterator)
        N = int(n_str)
        
        # Read A
        A = [int(next(iterator)) for _ in range(N)]
        
        # Read B
        B = [int(next(iterator)) for _ in range(N)]
        
        # Read C
        C = [int(next(iterator)) for _ in range(N)]
            
    except StopIteration:
        return

    # Calculate initial weighted sum S = sum(A_i * C_i)
    current_sum = 0
    for i in range(N):
        current_sum += A[i] * C[i]
        
    # Identify indices to flip
    # P: Indices where A[i] == 1 and B[i] == 0 (flip 1 -> 0, reduces sum)
    # Z: Indices where A[i] == 0 and B[i] == 1 (flip 0 -> 1, increases sum)
    
    P = [] # Stores C[i] for indices where A[i]=1, B[i]=0
    Z = [] # Stores C[i] for indices where A[i]=0, B[i]=1
    
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 1:
                P.append(C[i])
            else:
                Z.append(C[i])
    
    # Sort P descending (larger C first to reduce sum earlier)
    # This minimizes the cost because reducing the sum early lowers the cost of subsequent operations.
    P.sort(reverse=True)
    
    # Sort Z ascending (smaller C first to increase sum later)
    # This minimizes the cost because increasing the sum later means the higher sum is applied to fewer operations.
    Z.sort()
    
    total_cost = 0
    
    # Process P first
    for c in P:
        # Cost is current_sum after flip
        # Flip 1->0 reduces sum by c
        total_cost += current_sum - c
        current_sum -= c
        
    # Process Z second
    for c in Z:
        # Cost is current_sum after flip
        # Flip 0->1 increases sum by c
        total_cost += current_sum + c
        current_sum += c
        
    print(total_cost)

if __name__ == '__main__':
    solve()