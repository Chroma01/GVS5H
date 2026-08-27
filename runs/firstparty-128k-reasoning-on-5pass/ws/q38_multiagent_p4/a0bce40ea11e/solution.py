import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, p = data[0], data[1]
    vals = data[2:]
    A = [vals[i * n:(i + 1) * n] for i in range(n)]

    if p == 2:
        v = str(n & 1)
        line = " ".join([v] * n)
        sys.stdout.write("\n".join([line] * n))
        return

    K = 0
    for row in A:
        K += row.count(0)

    rn = range(n)
    m1 = p - 1

    def mat_mul(A, B, mod=p, n=n, rn=rn, m1=m1):
        C = [None] * n
        for i in rn:
            Ci = [0] * n
            Ai = A[i]
            for k in rn:
                aik = Ai[k]
                if aik:
                    Bk = B[k]
                    if aik == 1:
                        for j in rn:
                            Ci[j] += Bk[j]
                    elif aik == m1:
                        for j in rn:
                            Ci[j] -= Bk[j]
                    else:
                        for j in rn:
                            Ci[j] += aik * Bk[j]
            C[i] = [x % mod for x in Ci]
        return C

    res = A
    base = A
    e = p - 1
    while e:
        if e & 1:
            res = mat_mul(res, base)
        e >>= 1
        if e:
            base = mat_mul(base, base)

    M = res

    for i in rn:
        if A[i][i] == 0:
            Ai = A[i]
            Mi = M[i]
            for j in rn:
                if j == i:
                    continue

                val = Ai[j]
                if val:
                    x = Mi[j] + val
                    if x >= p:
                        x -= p
                    Mi[j] = x

                val = A[j][i]
                if val:
                    x = M[j][i] + val
                    if x >= p:
                        x -= p
                    M[j][i] = x

    if p == 3:
        for i in rn:
            Ai = A[i]
            Mi = M[i]
            for j in rn:
                if i != j and Ai[j] == 0:
                    val = A[j][i]
                    if val:
                        x = Mi[j] + val
                        if x >= p:
                            x -= p
                        Mi[j] = x

    if K & 1:
        for i in rn:
            Mi = M[i]
            for j in rn:
                if Mi[j]:
                    Mi[j] = p - Mi[j]

    sys.stdout.write("\n".join(" ".join(map(str, row)) for row in M))

if __name__ == "__main__":
    solve()