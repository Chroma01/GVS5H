import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    p = int(data[1])

    if p == 1:
        row = " ".join(["0"] * n)
        sys.stdout.write("\n".join([row] * n))
        return

    if p == 2:
        v = str(n & 1)
        row = " ".join([v] * n)
        sys.stdout.write("\n".join([row] * n))
        return

    A = []
    zeros = []
    zero_count = 0
    idx = 2

    for i in range(n):
        row = []
        for j in range(n):
            v = int(data[idx])
            idx += 1
            row.append(v)
            if v == 0:
                zero_count += 1
                zeros.append((i, j))
        A.append(row)

    mod = p
    rn = tuple(range(n))

    if sys.implementation.name == "cpython":
        from operator import mul

        def mat_mul(X, Y):
            Yt = list(zip(*Y))
            mod_local = mod
            mul_local = mul
            sum_local = sum
            map_local = map
            return [
                [sum_local(map_local(mul_local, Xi, Yj)) % mod_local for Yj in Yt]
                for Xi in X
            ]

    else:
        n4 = n - (n % 4)
        r4 = tuple(range(0, n4, 4))
        rt = tuple(range(n4, n))

        def mat_mul(X, Y):
            Z = [[0] * n for _ in range(n)]
            mod_local = mod
            r4_local = r4
            rt_local = rt
            rn_local = rn

            for i in rn_local:
                Xi = X[i]
                Zi = Z[i]

                for j in rn_local:
                    a = Xi[j]
                    if a:
                        Yj = Y[j]
                        for kk in r4_local:
                            Zi[kk] += a * Yj[kk]
                            Zi[kk + 1] += a * Yj[kk + 1]
                            Zi[kk + 2] += a * Yj[kk + 2]
                            Zi[kk + 3] += a * Yj[kk + 3]
                        for kk in rt_local:
                            Zi[kk] += a * Yj[kk]

                for kk in rn_local:
                    Zi[kk] %= mod_local

            return Z

    def mat_pow(M, e):
        result = None
        base = M

        while e:
            if e & 1:
                if result is None:
                    result = base
                else:
                    result = mat_mul(result, base)

            e >>= 1
            if e:
                base = mat_mul(base, base)

        return result

    M = mat_pow(A, p)

    if p == 3:
        for i, j in zeros:
            if i == j:
                Ai = A[i]
                for r in rn:
                    M[r][i] += A[r][i]
                    M[i][r] += Ai[r]
            else:
                M[i][j] += A[j][i]
    else:
        for i, j in zeros:
            if i == j:
                Ai = A[i]
                for r in rn:
                    M[r][i] += A[r][i]
                    M[i][r] += Ai[r]

    if zero_count & 1:
        for i in rn:
            Mi = M[i]
            for j in rn:
                Mi[j] = (-Mi[j]) % mod
    else:
        for i in rn:
            Mi = M[i]
            for j in rn:
                Mi[j] %= mod

    sys.stdout.write("\n".join(" ".join(map(str, M[i])) for i in rn))


if __name__ == "__main__":
    solve()