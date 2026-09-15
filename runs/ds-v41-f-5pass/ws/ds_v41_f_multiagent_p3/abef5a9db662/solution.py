import sys

def main():
    vals = list(map(int, sys.stdin.buffer.read().split()))
    n = vals[0]
    Ls = vals[1:1 + 2 * n:2]
    Rs = vals[2:1 + 2 * n:2]
    ptr = 1 + 2 * n
    qn = vals[ptr]
    ptr += 1
    Xs = vals[ptr:ptr + qn]
    M = max(Xs)

    SIZE = 1
    while SIZE < M:
        SIZE <<= 1
    NEG = -(1 << 60)
    sz2 = SIZE << 1
    sumE = [0] * sz2
    best = [0] * sz2

    for i in range(M):
        best[SIZE + i] = i + 1
    for i in range(M, SIZE):
        best[SIZE + i] = NEG
    for k in range(SIZE - 1, 0, -1):
        lc = k + k
        b = best[lc]
        alt = best[lc + 1]
        best[k] = b if b > alt else alt

    for i in range(n):
        L = Ls[i]
        if best[1] < L:
            continue
        R = Rs[i]
        k = 1; P = 0
        while k < SIZE:
            lc = k + k
            if P + best[lc] >= L:
                k = lc
            else:
                P += sumE[lc]
                k = lc + 1
        p = k - SIZE + 1
        T = R + 1
        if best[1] < T:
            q2 = M + 1
        else:
            k = 1; P = 0
            while k < SIZE:
                lc = k + k
                if P + best[lc] >= T:
                    k = lc
                else:
                    P += sumE[lc]
                    k = lc + 1
            q2 = k - SIZE + 1
        if q2 <= p:
            continue
        k = SIZE + p - 1
        se = sumE[k] + 1
        sumE[k] = se
        best[k] = se + p
        k >>= 1
        while k:
            lc = k + k
            s = sumE[lc] + sumE[lc + 1]
            sumE[k] = s
            b = best[lc]
            alt = sumE[lc] + best[lc + 1]
            if alt > b:
                b = alt
            best[k] = b
            k >>= 1
        if q2 <= M:
            k = SIZE + q2 - 1
            se = sumE[k] - 1
            sumE[k] = se
            best[k] = se + q2
            k >>= 1
            while k:
                lc = k + k
                s = sumE[lc] + sumE[lc + 1]
                sumE[k] = s
                b = best[lc]
                alt = sumE[lc] + best[lc + 1]
                if alt > b:
                    b = alt
                best[k] = b
                k >>= 1

    F = [0] * (M + 1)
    c = 0
    base = SIZE
    for x in range(1, M + 1):
        c += sumE[base + x - 1]
        F[x] = c + x

    out = []
    for x in Xs:
        out.append(F[x])
    sys.stdout.write('\n'.join(map(str, out)))
    sys.stdout.write('\n')

main()