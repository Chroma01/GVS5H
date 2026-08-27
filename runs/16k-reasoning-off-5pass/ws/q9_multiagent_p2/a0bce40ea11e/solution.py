import sys

# Increase recursion depth just in case, though iterative approach is used
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

    # Read matrix A
    A = []
    for _ in range(N):
        row = []
        for _ in range(N):
            row.append(int(next(iterator)))
        A.append(row)

    # Prepare matrix M based on p
    # Logic derived from properties of power sums in finite fields:
    # 1. If p = 2: The only non-zero value is 1. Replacing 0s with 1s in A gives matrix X.
    #    Since there is only 1 choice for each zero, the sum is simply X^2 mod 2.
    # 2. If p > 2: For any path in the expansion of B^p, if an edge corresponding to a zero 
    #    in A is used k times, its contribution involves sum_{x=1}^{p-1} x^k.
    #    This sum is 0 mod p unless p-1 divides k. Since path length is p (prime) and p > 2,
    #    p-1 does not divide p. The only surviving terms correspond to paths with NO zero edges.
    #    Thus, we treat zeros as 0 in the matrix M and compute M^p mod p.
    
    M = [[0] * N for _ in range(N)]
    
    if p == 2:
        for i in range(N):
            for j in range(N):
                if A[i][j] != 0:
                    M[i][j] = A[i][j] % 2
                else:
                    M[i][j] = 1 % 2
    else:
        for i in range(N):
            for j in range(N):
                if A[i][j] != 0:
                    M[i][j] = A[i][j] % p
                else:
                    M[i][j] = 0

    # Matrix multiplication function modulo p
    def mat_mul(X, Y, mod):
        size = len(X)
        Z = [[0] * size for _ in range(size)]
        for i in range(size):
            for k in range(size):
                if X[i][k] == 0:
                    continue
                val_x = X[i][k]
                for j in range(size):
                    Z[i][j] = (Z[i][j] + val_x * Y[k][j]) % mod
        return Z

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

    # Compute M^p
    result_matrix = mat_pow(M, p, p)

    # Output the result
    for i in range(N):
        row_str = " ".join(str(x) for x in result_matrix[i])
        print(row_str)

if __name__ == '__main__':
    solve()