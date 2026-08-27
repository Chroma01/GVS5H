import sys
from operator import mul

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    p = data[1]

    if p == 2:
        v = n % 2
        line = ' '.join(str(v) for _ in range(n))
        sys.stdout.write('\n'.join([line] * n))
        return

    C = []
    parity = 0
    all_zero = True
    idx = 2
    for i in range(n):
        row = []
        for j in range(n):
            x = data[idx]
            idx += 1
            row.append(x)
            if x == 0:
                parity ^= 1
            else:
                all_zero = False
        C.append(row)

    if all_zero:
        line = ' '.join(['0'] * n)
        sys.stdout.write('\n'.join([line] * n))
        return

    if n == 1:
        sys.stdout.write(str(C[0][0] % p))
        return

    def matmul(X, Y, mod, mul=mul, sum=sum, map=map, zip=zip):
        yt = list(zip(*Y))
        return [[sum(map(mul, row, col)) % mod for col in yt] for row in X]

    result = C
    base = C
    e = p - 1
    while e:
        if e & 1:
            result = matmul(result, base, p)
        e >>= 1
        if e:
            base = matmul(base, base, p)
    P = result

    V = [[0] * n for _ in range(n)]

    if p == 3:
        for i in range(n):
            Ci = C[i]
            Vi = V[i]
            for j in range(n):
                if Ci[j] == 0:
                    if i == j:
                        for t in range(n):
                            Vi[t] += Ci[t]
                        for t in range(n):
                            V[t][i] += C[t][i]
                    else:
                        Vi[j] += C[j][i]
    else:
        for i in range(n):
            Ci = C[i]
            Vi = V[i]
            if Ci[i] == 0:
                for t in range(n):
                    Vi[t] += Ci[t]
                for t in range(n):
                    V[t][i] += C[t][i]

    sign = 1 if parity == 0 else p - 1
    out_lines = []

    if sign == 1:
        for i in range(n):
            Pi = P[i]
            Vi = V[i]
            out_lines.append(' '.join(str((Pi[j] + Vi[j]) % p) for j in range(n)))
    else:
        for i in range(n):
            Pi = P[i]
            Vi = V[i]
            row = []
            for j in range(n):
                val = (Pi[j] + Vi[j]) % p
                if val:
                    val = p - val
                row.append(str(val))
            out_lines.append(' '.join(row))

    sys.stdout.write('\n'.join(out_lines))

if __name__ == '__main__':
    main()