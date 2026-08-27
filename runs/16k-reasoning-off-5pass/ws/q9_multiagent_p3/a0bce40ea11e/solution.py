import sys

# Increase recursion depth just in case, though we use iterative approach
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

    # Calculate the scaling factor: (p-1)^K mod p
    # Since p is prime, (p-1) = -1 mod p. So factor is (-1)^K mod p.
    # If K is even, factor is 1. If K is odd, factor is p-1 (which is -1 mod p).
    if K % 2 == 0:
        factor = 1
    else:
        factor = p - 1

    # Matrix multiplication function
    def mat_mul(X, Y, mod):
        size = len(X)
        # Initialize result matrix with zeros
        res = [[0] * size for _ in range(size)]
        
        for i in range(size):
            for k in range(size):
                if X[i][k] == 0:
                    continue
                val_x = X[i][k]
                for j in range(size):
                    if Y[k][j] == 0:
                        continue
                    res[i][j] = (res[i][j] + val_x * Y[k][j]) % mod
        return res

    # Matrix exponentiation function
    def mat_pow(X, power, mod):
        size = len(X)
        # Identity matrix
        res = [[0] * size for _ in range(size)]
        for i in range(size):
            res[i][i] = 1
            
        base = X
        while power > 0:
            if power % 2 == 1:
                res = mat_mul(res, base, mod)
            base = mat_mul(base, base, mod)
            power //= 2
        return res

    # Prepare matrix M: same as A, but 0s are treated as 0 (which they already are)
    # The logic derived is:
    # Sum = (p-1)^K * (Sum of products of paths of length p using only non-zero entries)
    # The sum of products of paths of length p using only non-zero entries is exactly (M^p)_{i,j}
    # where M has 0s where A has 0s.
    # So we just compute A^p (treating 0s as 0) and multiply by factor.
    
    M = [row[:] for row in A] # Copy A
    
    # Compute M^p mod p
    M_p = mat_pow(M, p, p)
    
    # Multiply each element by factor
    result = []
    for i in range(N):
        row_res = []
        for j in range(N):
            val = (M_p[i][j] * factor) % p
            row_res.append(str(val))
        result.append(" ".join(row_res))
    
    # Print the result
    for line in result:
        print(line)

if __name__ == '__main__':
    solve()