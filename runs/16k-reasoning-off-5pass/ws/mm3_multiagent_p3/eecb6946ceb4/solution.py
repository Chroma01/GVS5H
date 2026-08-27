import sys
import cmath
import math

def fft(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        ang = 2 * math.pi / length * (-1 if invert else 1)
        wlen = cmath.rect(1, ang)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w
                a[j] = u + v
                a[j + half] = u - v
                w *= wlen
        length <<= 1
    if invert:
        for i in range(n):
            a[i] /= n

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    S = [int(next(it)) for _ in range(N)]
    if N < 3:
        print(0)
        return
    M = max(S)
    size = 1
    while size <= 2 * M:
        size <<= 1
    fa = [0j] * size
    for x in S:
        fa[x] = 1
    fft(fa, False)
    for i in range(size):
        fa[i] *= fa[i]
    fft(fa, True)
    ans = 0
    for b in S:
        cnt = int(round(fa[2 * b].real))
        ans += cnt // 2
    print(ans)

if __name__ == "__main__":
    solve()