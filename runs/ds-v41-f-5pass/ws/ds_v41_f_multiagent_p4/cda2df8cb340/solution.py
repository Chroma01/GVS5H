import sys
from collections import Counter

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    ca = Counter(A)
    vals = list(ca.keys())
    mults = list(ca.values())
    D = len(vals)

    maxA = max(vals)
    maxsum = maxA * 2

    # diagonal contribution: sum of odd part of A_i (pairs i == i)
    diag = 0
    for v, m in zip(vals, mults):
        diag += (v // (v & -v)) * m

    ordered = 0          # sum over ALL ordered pairs (i, j) of f(A_i + A_j)
    LIM = 1 << 20
    k = 0
    while (1 << k) <= maxsum:
        half = 1 << k
        M = half << 1
        mask = M - 1

        if M <= LIM and M <= 8 * D:
            cnt = [0] * M
            for v, m in zip(vals, mults):
                cnt[v & mask] += m
            s = 0
            for v, m in zip(vals, mults):
                c = cnt[(half - v) & mask]
                if c:
                    s += v * m * c
        else:
            cnt = {}
            get = cnt.get
            for v, m in zip(vals, mults):
                r = v & mask
                cnt[r] = get(r, 0) + m
            g = cnt.get
            s = 0
            for v, m in zip(vals, mults):
                c = g((half - v) & mask, 0)
                if c:
                    s += v * m * c

        # s = sum over ordered pairs with v2 = k of A_i
        # contribution = sum (A_i + A_j)/2^k = 2*s / half
        ordered += (s << 1) // half
        k += 1

    # answer = sum_{i<=j} = (ordered + diag) / 2
    sys.stdout.write(str((ordered + diag) >> 1) + "\n")

main()