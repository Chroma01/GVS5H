import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    p = int(next(it))
    A = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(next(it)))
        A.append(row)
    
    if p == 2:
        # For p=2, each zero is replaced by 1 (only option)
        B = [[1 if A[i][j] == 0 else A[i][j] for j in range(N)] for i in range(N)]
        # Compute B^2 mod 2
        def mat_mul(X, Y, mod):
            n = len(X)
            Z = [[0]*n for _ in range(n)]
            for i in range(n):
                for k in range(n):
                    if X[i][k] == 0:
                        continue
                    for j in range(n):
                        Z[i][j] = (Z[i][j] + X[i][k] * Y[k][j]) % mod
            return Z
        
        B2 = mat_mul(B, B, 2)
        for i in range(N):
            print(' '.join(str(x) for x in B2[i]))
        return
    
    # For p>2
    # Let M be A with zeros replaced by 0.
    M = [[0 if A[i][j] == 0 else A[i][j] for j in range(N)] for i in range(N)]
    
    # Compute T = M^p mod p
    def mat_mul(X, Y, mod):
        n = len(X)
        Z = [[0]*n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                if X[i][k] == 0:
                    continue
                for j in range(n):
                    Z[i][j] = (Z[i][j] + X[i][k] * Y[k][j]) % mod
        return Z
    
    def mat_pow(X, power, mod):
        n = len(X)
        result = [[0]*n for _ in range(n)]
        for i in range(n):
            result[i][i] = 1
        base = X
        while power > 0:
            if power % 2 == 1:
                result = mat_mul(result, base, mod)
            base = mat_mul(base, base, mod)
            power //= 2
        return result
    
    T = mat_pow(M, p, p)
    
    # Find zero positions
    zeros = []
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                zeros.append((i,j))
    
    sign = 1
    if len(zeros) % 2 == 1:
        sign = p - 1  # -1 mod p
    
    S = [row[:] for row in T]
    
    for (u,v) in zeros:
        if u == v:
            # Self-loop zero
            for i in range(N):
                if A[i][u] != 0:
                    S[i][u] = (S[i][u] + sign * A[i][u]) % p
            for j in range(N):
                if A[u][j] != 0:
                    S[u][j] = (S[u][j] + sign * A[u][j]) % p
        # For non-self-loop zeros with p>2, no contribution as derived
    
    # Output
    for i in range(N):
        print(' '.join(str(x) for x in S[i]))

if __name__ == '__main__':
    main()