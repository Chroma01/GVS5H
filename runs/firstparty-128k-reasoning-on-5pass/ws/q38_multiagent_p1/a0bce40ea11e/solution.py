import sys
from operator import mul


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    p = int(data[1])

    if p == 1:
        line = ' '.join(['0'] * N)
        sys.stdout.write('\n'.join([line] * N))
        return

    if p == 2:
        v = str(N & 1)
        line = ' '.join([v] * N)
        sys.stdout.write('\n'.join([line] * N))
        return

    C = [[0] * N for _ in range(N)]
    zero_diag = [False] * N
    zero_off = []
    K = 0
    has_nonzero = False
    offdiag_nonzero = False

    idx = 2
    for i in range(N):
        Ci = C[i]
        for j in range(N):
            v = int(data[idx])
            idx += 1
            if v == 0:
                K += 1
                if i == j:
                    zero_diag[i] = True
                else:
                    zero_off.append((i, j))
            else:
                Ci[j] = v % p
                has_nonzero = True
                if i != j:
                    offdiag_nonzero = True

    def matmul(A, B, mod):
        Bt = list(zip(*B))
        mul_local = mul
        return [[sum(map(mul_local, row, col)) % mod for col in Bt] for row in A]

    def mat_pow(base, exp, mod):
        res = None
        e = exp
        while e:
            if e & 1:
                if res is None:
                    res = [row[:] for row in base]
                else:
                    res = matmul(res, base, mod)
            e >>= 1
            if e:
                base = matmul(base, base, mod)

        if res is None:
            res = [[0] * N for _ in range(N)]
            for i in range(N):
                res[i][i] = 1 % mod
        return res

    if not has_nonzero:
        P = [[0] * N for _ in range(N)]
    elif not offdiag_nonzero:
        P = [[0] * N for _ in range(N)]
        for i in range(N):
            P[i][i] = pow(C[i][i], p, p)
    else:
        P = mat_pow(C, p, p)

    if offdiag_nonzero:
        for r in range(N):
            if zero_diag[r]:
                row = C[r]
                Pr = P[r]

                for b in range(N):
                    if b != r:
                        val = row[b]
                        if val:
                            x = Pr[b] + val
                            if x >= p:
                                x -= p
                            Pr[b] = x

                for a in range(N):
                    if a != r:
                        val = C[a][r]
                        if val:
                            x = P[a][r] + val
                            if x >= p:
                                x -= p
                            P[a][r] = x

        if p == 3:
            for u, v in zero_off:
                val = C[v][u]
                if val:
                    x = P[u][v] + val
                    if x >= p:
                        x -= p
                    P[u][v] = x

    if K & 1:
        for i in range(N):
            Pi = P[i]
            for j in range(N):
                x = Pi[j]
                if x:
                    Pi[j] = p - x

    sys.stdout.write('\n'.join(' '.join(map(str, row)) for row in P))


if __name__ == "__main__":
    solve()