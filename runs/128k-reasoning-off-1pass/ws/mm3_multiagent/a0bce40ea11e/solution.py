import sys
import numpy as np

def solve():
    input = sys.stdin.readline
    N, p = map(int, input().split())
    A = []
    for _ in range(N):
        A.append(list(map(int, input().split())))
    K = sum(1 for i in range(N) for j in range(N) if A[i][j] == 0)
    
    if p == 2:
        # For p=2, the sum is simply (A')^2 mod 2, where A' has 1 at zero positions
        A2 = [[1 if A[i][j] == 0 else A[i][j] for j in range(N)] for i in range(N)]
        M = np.array(A2, dtype=np.int64)
        P = np.dot(M, M) % 2
        for row in P:
            print(' '.join(map(str, row)))
        return
    
    # Build M: zeros remain zero, nonzeros keep their value
    M = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if A[i][j] != 0:
                M[i][j] = A[i][j]
    M_np = np.array(M, dtype=np.int64)
    
    # Compute P = M^p mod p
    P = np.eye(N, dtype=np.int64)
    base = M_np.copy()
    exp = p
    while exp > 0:
        if exp & 1:
            P = np.dot(P, base) % p
        base = np.dot(base, base) % p
        exp >>= 1
    
    # Compute D matrix for Type B contributions
    D = np.zeros((N, N), dtype=np.int64)
    for r in range(N):
        for c in range(N):
            if A[r][c] == 0:
                if r == c:
                    # Diagonal zero: add A[u][r] to D[u][r] for u with A[u][r] != 0
                    for u in range(N):
                        if A[u][r] != 0:
                            D[u, r] = (D[u, r] + A[u][r]) % p
                    # Add A[r][v] to D[r][v] for v with A[r][v] != 0
                    for v in range(N):
                        if A[r][v] != 0:
                            D[r, v] = (D[r, v] + A[r][v]) % p
                elif p == 3:
                    # Off-diagonal zero: only contributes for p=3
                    if A[c][r] != 0:
                        D[r, c] = (D[r, c] + A[c][r]) % p
    
    # Compute sign: (-1)^K mod p
    sign = 1 if K % 2 == 0 else p - 1
    
    # Result = sign * (P + D) mod p
    Result = (sign * (P + D)) % p
    
    for row in Result:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    solve()