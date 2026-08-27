import sys
import gc

def matmul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    rng = range(n)
    m1 = mod - 1
    bit = (mod == 2)
    for i in rng:
        Ci = C[i]
        Ai = A[i]
        for k in rng:
            aik = Ai[k]
            if aik:
                Bk = B[k]
                if aik == 1:
                    for j in rng:
                        Ci[j] += Bk[j]
                elif aik == m1:
                    for j in rng:
                        Ci[j] -= Bk[j]
                else:
                    for j in rng:
                        Ci[j] += aik * Bk[j]
        if bit:
            C[i] = [x & 1 for x in Ci]
        else:
            C[i] = [x % mod for x in Ci]
    return C

def mat_pow(F, p, mod):
    result = F
    bl = p.bit_length()
    for b in range(bl - 2, -1, -1):
        result = matmul(result, result, mod)
        if (p >> b) & 1:
            result = matmul(F, result, mod)
    return result

def main():
    gc.disable()
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    p = data[1]

    if p == 1:
        line = ' '.join(['0'] * N)
        sys.stdout.write('\n'.join([line] * N))
        return

    if p == 2:
        B = []
        idx = 2
        for _ in range(N):
            row = []
            for _ in range(N):
                x = data[idx]
                idx += 1
                if x == 0:
                    row.append(1)
                else:
                    row.append(x & 1)
            B.append(row)
        P = matmul(B, B, 2)
        sys.stdout.write('\n'.join(' '.join(str(x) for x in row) for row in P))
        return

    vals = data[2:]
    F = []
    K = 0
    idx = 0
    for _ in range(N):
        row = []
        for _ in range(N):
            x = vals[idx]
            idx += 1
            if x == 0:
                K += 1
            row.append(x)
        F.append(row)

    P = mat_pow(F, p, p)

    C = [[0] * N for _ in range(N)]
    rng = range(N)

    for i in rng:
        if F[i][i] == 0:
            for r in rng:
                C[r][i] += F[r][i]
            Fi = F[i]
            Ci = C[i]
            for c in rng:
                Ci[c] += Fi[c]

    if p == 3:
        for i in rng:
            Fi = F[i]
            Ci = C[i]
            for j in rng:
                if i != j and Fi[j] == 0:
                    Ci[j] += F[j][i]

    lines = []
    if K & 1:
        for i in rng:
            Pi = P[i]
            Ci = C[i]
            lines.append(' '.join(str((-(Pi[j] + Ci[j])) % p) for j in rng))
    else:
        for i in rng:
            Pi = P[i]
            Ci = C[i]
            lines.append(' '.join(str((Pi[j] + Ci[j]) % p) for j in rng))

    sys.stdout.write('\n'.join(lines))

if __name__ == '__main__':
    main()