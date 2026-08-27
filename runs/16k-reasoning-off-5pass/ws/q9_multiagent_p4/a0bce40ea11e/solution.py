import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        p = int(next(iterator))
    except StopIteration:
        return

    A = []
    for _ in range(N):
        row = []
        for _ in range(N):
            row.append(int(next(iterator)))
        A.append(row)

    # Count the number of zeros in A
    K = 0
    for r in range(N):
        for c in range(N):
            if A[r][c] == 0:
                K += 1

    # Logic based on Fermat's Little Theorem: x^p = x (mod p)
    # The sum of B^p over all B is equivalent to the sum of B over all B (mod p).
    # For a cell (i, j):
    # 1. If A[i][j] != 0: It is fixed. It appears (p-1)^K times.
    #    Contribution = A[i][j] * (p-1)^K
    # 2. If A[i][j] == 0: It takes values 1..p-1. Each value appears (p-1)^(K-1) times.
    #    Contribution = (p-1)^(K-1) * sum(1..p-1)
    #    sum(1..p-1) = p*(p-1)/2.
    #    If p > 2, p*(p-1)/2 is divisible by p, so sum = 0 (mod p).
    #    If p = 2, sum = 1. (p-1)^(K-1) = 1^(K-1) = 1. Contribution = 1.
    
    if p == 2:
        # For p=2, every cell becomes 1.
        # If A[i][j] was 0 -> contribution 1.
        # If A[i][j] was 1 -> contribution 1 * 1^K = 1.
        result = [[1] * N for _ in range(N)]
    else:
        # For p > 2, zeros contribute 0. Non-zeros contribute A[i][j] * (p-1)^K.
        # Calculate (p-1)^K mod p
        term = pow(p - 1, K, p)
        
        result = []
        for r in range(N):
            row_res = []
            for c in range(N):
                if A[r][c] == 0:
                    row_res.append(0)
                else:
                    val = (A[r][c] * term) % p
                    row_res.append(val)
            result.append(row_res)

    # Print the result
    for row in result:
        print(*(row))

if __name__ == '__main__':
    solve()