import sys

MOD = 998244353
G = 3

def ntt(a, invert):
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
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    S = [int(next(it)) for _ in range(n)]
    if n < 3:
        print(0)
        return
    max_val = max(S)
    size = 1
    while size <= 2 * max_val:
        size <<= 1
    a = [0] * size
    for x in S:
        a[x] = 1
    ntt(a, False)
    for i in range(size):
        a[i] = a[i] * a[i] % MOD
    ntt(a, True)
    ans = 0
    for b in S:
        ans += (a[2 * b] - 1) // 2
    print(ans)

if __name__ == "__main__":
    solve()