import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    A = list(map(int, data[pos:pos + n])); pos += n
    q = int(data[pos]); pos += 1

    INF = n + 1
    # d[i] = distance to first j >= i with A[j] >= 2*A[i], else INF
    d = [INF] * n
    for i in range(n):
        j = bisect_left(A, 2 * A[i], i)
        if j < n:
            d[i] = j - i

    # sparse table for range maximum of d
    sp = [d]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        half = 1 << (k - 1)
        width = 1 << k
        sp.append([prev[i] if prev[i] >= prev[i + half] else prev[i + half]
                   for i in range(n - width + 1)])
        k += 1

    log2 = [0] * (n + 1)
    for i in range(2, n + 1):
        log2[i] = log2[i >> 1] + 1

    out = []
    for _ in range(q):
        L = int(data[pos]) - 1
        R = int(data[pos + 1]) - 1
        pos += 2
        M = R - L + 1
        lo, hi = 0, M >> 1
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            kk = log2[mid]
            row = sp[kk]
            a = row[L]
            b = row[L + mid - (1 << kk)]
            mx = a if a >= b else b
            if mx <= M - mid:
                lo = mid
            else:
                hi = mid - 1
        out.append(lo)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()