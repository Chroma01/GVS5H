import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    p = int(data[pos]); pos += 1
    A = []
    for _ in range(N):
        row = list(map(int, data[pos:pos + N]))
        pos += N
        A.append(row)

    K = 0
    for i in range(N):
        Ai = A[i]
        for j in range(N):
            if Ai[j] == 0:
                K += 1

    # p = 2: only nonzero value is 1, so the unique completion is the all-ones
    # matrix J, and J^2 = N*J  =>  every entry is N mod 2.
    if p == 2:
        v = N & 1
        line = ' '.join([str(v)] * N)
        sys.stdout.write('\n'.join([line] * N) + '\n')
        return

    def compute_power():
        """Return C^p mod p as a list of lists, where C = A (zeros kept as 0)."""
        try:
            import numpy as np
        except Exception:
            np = None

        if np is not None:
            Anp = np.array(A, dtype=np.int64) % p
            shift = (1 << 15) % p

            def matmul(X, Y):
                Y1 = Y >> 15
                Y0 = Y & 32767
                t1 = (X @ Y1) % p
                t0 = (X @ Y0) % p
                return (t1 * shift + t0) % p

            result = np.eye(N, dtype=np.int64) % p
            base = Anp.copy()
            e = p
            while e > 0:
                if e & 1:
                    result = matmul(result, base)
                e >>= 1
                if e:
                    base = matmul(base, base)
            return result.tolist()
        else:
            def matmul(X, Y):
                n = len(X)
                Z = [[0] * n for _ in range(n)]
                for i in range(n):
                    Xi = X[i]
                    Zi = Z[i]
                    for k in range(n):
                        a = Xi[k]
                        if a:
                            Yk = Y[k]
                            for j in range(n):
                                Zi[j] += a * Yk[j]
                    for j in range(n):
                        Zi[j] %= p
                return Z

            result = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
            base = [row[:] for row in A]
            e = p
            while e > 0:
                if e & 1:
                    result = matmul(result, base)
                e >>= 1
                if e:
                    base = matmul(base, base)
            return result

    M = compute_power()

    # Corrections for walks that use exactly one zero-variable p-1 times
    # (the only surviving monomials besides all-constant walks).
    if p == 3:
        # A variable used twice; the remaining step may bridge the two uses.
        for u in range(N):
            for v in range(N):
                if A[u][v] == 0:
                    if u == v:
                        # loop-then-leave (row u) and enter-then-loop (column u)
                        for j in range(N):
                            M[u][j] = (M[u][j] + A[u][j]) % p
                            M[j][u] = (M[j][u] + A[j][u]) % p
                    else:
                        # u ->v (var) v->u (const) u->v (var)
                        M[u][v] = (M[u][v] + A[v][u]) % p
    else:
        # p >= 5: only diagonal zeros can be used p-1 times, always as a loop,
        # with the single constant edge at the very start or very end.
        for u in range(N):
            if A[u][u] == 0:
                for j in range(N):
                    M[u][j] = (M[u][j] + A[u][j]) % p   # leave after loops
                    M[j][u] = (M[j][u] + A[j][u]) % p   # enter before loops

    # Every zero variable contributes sum_{x in F_p^*} x^e = -1 when (p-1)|e.
    sign = pow(p - 1, K, p)
    if sign != 1:
        for i in range(N):
            Mi = M[i]
            for j in range(N):
                Mi[j] = Mi[j] * sign % p

    sys.stdout.write('\n'.join(' '.join(map(str, row)) for row in M) + '\n')

main()