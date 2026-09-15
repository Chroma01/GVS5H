import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    p = int(data[1])

    A = []
    zero_positions = []
    has_offdiag_nonzero = False
    idx = 2

    for i in range(N):
        row = []
        for j in range(N):
            v = int(data[idx])
            idx += 1
            row.append(v)
            if v == 0:
                zero_positions.append((i, j))
            elif i != j:
                has_offdiag_nonzero = True
        A.append(row)

    K = len(zero_positions)

    if p <= 1:
        line = " ".join(["0"] * N)
        sys.stdout.write("\n".join([line] * N))
        return

    # For p = 2, every entry becomes 1, so B is the all-ones matrix.
    if p == 2:
        val = str(N & 1)
        line = " ".join([val] * N)
        sys.stdout.write("\n".join([line] * N))
        return

    # Odd prime. If A is all zero, all surviving terms are zero.
    if K == N * N:
        line = " ".join(["0"] * N)
        sys.stdout.write("\n".join([line] * N))
        return

    # If A is diagonal, A^p = A over F_p.
    if not has_offdiag_nonzero:
        Ap = [[0] * N for _ in range(N)]
        for i in range(N):
            Ap[i][i] = A[i][i]
    else:
        use_numpy = False

        # Optional fast path for CPython when numpy is available.
        if not hasattr(sys, "pypy_version_info") and N >= 60 and p > 10000:
            try:
                import numpy as np
                use_numpy = True
            except Exception:
                use_numpy = False

        if use_numpy:
            n = N
            prod = (p - 1) * (p - 1)
            if prod == 0:
                chunk = n
            else:
                # Keep every int64 accumulation below 2^63.
                limit = (1 << 63) - 1 - p - 1
                chunk = limit // prod
                if chunk < 1:
                    chunk = 1
                if chunk > n:
                    chunk = n

            def matmul_np(X, Y):
                if chunk >= n:
                    return (X @ Y) % p
                Z = np.zeros((n, n), dtype=np.int64)
                for s in range(0, n, chunk):
                    e = s + chunk
                    if e > n:
                        e = n
                    Z += X[:, s:e] @ Y[s:e, :]
                    Z %= p
                return Z

            base = np.array(A, dtype=np.int64)
            res = base.copy()
            e = p - 1

            # Compute A * A^(p-1).
            while e:
                if e & 1:
                    res = matmul_np(res, base)
                e >>= 1
                if e:
                    base = matmul_np(base, base)

            Ap = res.tolist()

        else:
            # Pure Python fallback.
            if hasattr(sys, "pypy_version_info"):
                def mat_mul(X, Y, mod):
                    n = len(X)
                    Z = [[0] * n for _ in range(n)]
                    rng = range(n)
                    for i in rng:
                        Zi = Z[i]
                        Xi = X[i]
                        for k in rng:
                            a = Xi[k]
                            if a:
                                Yk = Y[k]
                                for j in rng:
                                    Zi[j] += a * Yk[j]
                        for j in rng:
                            Zi[j] %= mod
                    return Z
            else:
                from operator import mul

                def mat_mul_sparse(X, Y, mod):
                    n = len(X)
                    Z = [[0] * n for _ in range(n)]
                    rng = range(n)
                    for i in rng:
                        Zi = Z[i]
                        Xi = X[i]
                        for k in rng:
                            a = Xi[k]
                            if a:
                                Yk = Y[k]
                                for j in rng:
                                    Zi[j] += a * Yk[j]
                        for j in rng:
                            Zi[j] %= mod
                    return Z

                def mat_mul_dense(X, Y, mod):
                    Yt = list(zip(*Y))
                    mul_func = mul
                    return [
                        [sum(map(mul_func, row, col)) % mod for col in Yt]
                        for row in X
                    ]

                def mat_mul(X, Y, mod):
                    n = len(X)
                    zero_count = 0
                    for row in X:
                        zero_count += row.count(0)

                    if zero_count == n * n:
                        return [[0] * n for _ in range(n)]

                    # Use sparse multiplication when X is quite sparse.
                    if zero_count * 4 >= n * n * 3:
                        return mat_mul_sparse(X, Y, mod)
                    return mat_mul_dense(X, Y, mod)

            res = [row[:] for row in A]
            base = A
            e = p - 1

            while e:
                if e & 1:
                    res = mat_mul(res, base, p)
                e >>= 1
                if e:
                    base = mat_mul(base, base, p)

            Ap = res

    # Add surviving correction terms.
    if p == 3:
        for i, j in zero_positions:
            if i == j:
                Ai = A[i]
                for r in range(N):
                    Ap[r][i] += A[r][i]
                    Ap[i][r] += Ai[r]
            else:
                Ap[i][j] += A[j][i]
    else:
        for i, j in zero_positions:
            if i == j:
                Ai = A[i]
                for r in range(N):
                    Ap[r][i] += A[r][i]
                    Ap[i][r] += Ai[r]

    # Apply global sign (-1)^K and output.
    lines = []
    if K & 1:
        for i in range(N):
            row = Ap[i]
            out = []
            for j in range(N):
                v = row[j] % p
                if v:
                    v = p - v
                out.append(str(v))
            lines.append(" ".join(out))
    else:
        for i in range(N):
            row = Ap[i]
            out = [str(row[j] % p) for j in range(N)]
            lines.append(" ".join(out))

    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    solve()