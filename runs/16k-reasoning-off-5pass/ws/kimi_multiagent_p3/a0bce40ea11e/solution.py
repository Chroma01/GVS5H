import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); p = int(data[pos + 1]); pos += 2
    A = [[int(data[pos + i * n + j]) % p for j in range(n)] for i in range(n)]
    pos += n * n

    # matrix multiply mod p, O(n^3)
    def matmul(X, Y):
        Z = [[0] * n for _ in range(n)]
        for i in range(n):
            Xi = X[i]
            Zi = Z[i]
            for k in range(n):
                x = Xi[k]
                if x:
                    Yk = Y[k]
                    xv = x
                    for j in range(n):
                        Zi[j] = (Zi[j] + xv * Yk[j]) % p
        return Z

    def matpow(M, e):
        R = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        B = [row[:] for row in M]
        while e:
            if e & 1:
                R = matmul(R, B)
            e >>= 1
            if e:
                B = matmul(B, B)
        return R

    K = 0
    for i in range(n):
        Ai = A[i]
        for j in range(n):
            if Ai[j] == 0:
                K += 1

    if p == 2:
        # unique filling: zeros become 1; answer is B^2 mod 2
        B = [[A[i][j] if A[i][j] else 1 for j in range(n)] for i in range(n)]
        C = matmul(B, B)
    else:
        # S = (-1)^K * ( A^p + loop-correction + (p==3 ? non-loop-correction : 0) ) mod p
        C = matpow(A, p)
        # loop zeros e=(u,u): contribute A E_uu + E_uu A
        # (the (p-2)*E F E term vanishes since A[u][u] = 0)
        for u in range(n):
            if A[u][u] == 0:
                Au = A[u]
                Cu = C[u]
                for j in range(n):
                    Cu[j] = (Cu[j] + Au[j]) % p      # E_uu A: row u += row u of A
                for i in range(n):
                    C[i][u] = (C[i][u] + A[i][u]) % p  # A E_uu: col u += col u of A
        # non-loop zeros contribute only when p == 3: A[v][u] * E_{u,v}
        if p == 3:
            for u in range(n):
                Au = A[u]
                Cu = C[u]
                for v in range(n):
                    if u != v and Au[v] == 0:
                        Cu[v] = (Cu[v] + A[v][u]) % p
        if K & 1:
            # multiply by (-1)^K = -1 mod p
            for i in range(n):
                Ci = C[i]
                for j in range(n):
                    if Ci[j]:
                        Ci[j] = p - Ci[j]

    out = sys.stdout
    for i in range(n):
        out.write(' '.join(map(str, C[i])) + '\n')

main()