import sys

# Increase recursion depth just in case, though we use iterative exponentiation
sys.setrecursionlimit(2000)

def mat_mul(A, B, p, n):
    """Multiply two n x n matrices modulo p."""
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k] == 0:
                continue
            val_a = A[i][k]
            for j in range(n):
                C[i][j] = (C[i][j] + val_a * B[k][j]) % p
    return C

def mat_pow(A, p, n):
    """Compute A^p modulo p using binary exponentiation."""
    # Initialize result as identity matrix
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    
    base = [row[:] for row in A]
    
    while p > 0:
        if p % 2 == 1:
            res = mat_mul(res, base, p, n)
        base = mat_mul(base, base, p, n)
        p //= 2
    return res

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

    # Step 1: Compute A^p mod p
    # Note: In the problem, we sum B^p.
    # If A has no zeros, the sum is just A^p (since there's only one B=A).
    # If A has zeros, we use the derived logic:
    # Sum = (A^p treating 0 as 0) + corrections for diagonal zeros.
    
    # Compute A^p
    # We treat 0^k as 0 for k >= 1.
    # Python's pow(0, k, p) handles 0^k correctly for k>=1 (returns 0).
    # However, for matrix multiplication, we just use the values in A.
    # If A[i][j] is 0, it contributes 0 to the product.
    
    Ap = mat_pow(A, p, N)
    
    # Step 2: Apply corrections for diagonal zeros
    # Logic: If A[i][i] == 0, then for any j != i, we add:
    #   - A[i][j] if A[i][j] != 0
    #   - 1 if A[i][j] == 0
    # This is derived from the fact that the only non-zero contributions from
    # walks involving a zero at (i,i) occur when the zero is traversed p-1 times
    # and one other edge (i,j) is traversed 1 time.
    # The contribution is (-1) * (value of edge (i,j)).
    # If (i,j) is non-zero, value is A[i][j], so -A[i][j].
    # If (i,j) is zero, value is sum_{x=1}^{p-1} x^1 = -1, so -(-1) = 1.
    
    result = [row[:] for row in Ap]
    
    for i in range(N):
        if A[i][i] == 0:
            for j in range(N):
                if i == j:
                    continue
                if A[i][j] != 0:
                    val = -A[i][j]
                else:
                    val = 1
                result[i][j] = (result[i][j] + val) % p
                
    # Output the result
    for i in range(N):
        print(*(result[i]))

if __name__ == '__main__':
    solve()