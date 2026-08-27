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

        half = length >> 1
        for start in range(0, n, length):
            w = 1
            end = start + half
            for i in range(start, end):
                u = a[i]
                v = a[i + half] * w % MOD
                a[i] = (u + v) % MOD
                a[i + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def add_convolution(acc, f, fact, t, l, m, r):
    width = m - l
    min_t = t[m]
    max_x = t[r - 1] - min_t
    h_len = max_x + width + 1

    # For source i=l+a and query q with x=t[q]-min_t:
    # fact[t[q]-i] = H[x + width - a],
    # where H[u] = fact[min_t + u - width].
    work = width * h_len
    if work <= 256:
        for q in range(m, r):
            tq = t[q]
            total = 0
            for i in range(l, m):
                k = tq - i
                if 0 <= k < len(fact):
                    total += f[i] * fact[k]
            acc[q] = (acc[q] + total) % MOD
        return

    size = 1
    need = width + h_len - 1
    while size < need:
        size <<= 1

    a = [0] * size
    b = [0] * size

    for i in range(width):
        a[i] = f[l + i]

    for u in range(h_len):
        k = min_t + u - width
        if 0 <= k < len(fact):
            b[u] = fact[k]

    ntt(a, False)
    ntt(b, False)
    for i in range(size):
        a[i] = a[i] * b[i] % MOD
    ntt(a, True)

    for q in range(m, r):
        idx = t[q] - min_t + width
        acc[q] = (acc[q] + a[idx]) % MOD


def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    if s[0] != "B" or s[-1] != "W":
        print(0)
        return

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # t[j] is the number of W's before the (j+1)-st B.
    t = [0] * n
    whites = 0
    blacks = 0
    for c in s:
        if c == "W":
            whites += 1
        else:
            blacks += 1
            if blacks >= 2:
                t[blacks - 1] = whites

    for j in range(1, n):
        if t[j] == n:
            print(0)
            return

    f = [0] * n
    acc = [0] * n
    f[0] = 1

    sys.setrecursionlimit(1_000_000)

    def cdq(l, r):
        if r - l == 1:
            if l == 0:
                return
            if t[l] < l:
                f[l] = 0
            else:
                f[l] = -acc[l] * inv_fact[t[l] - l] % MOD
            return

        m = (l + r) >> 1
        cdq(l, m)
        add_convolution(acc, f, fact, t, l, m, r)
        cdq(m, r)

    cdq(0, n)

    ans = fact[n]
    for j in range(1, n):
        ans = (ans + f[j] * fact[n - j]) % MOD
    print(ans)


if __name__ == "__main__":
    solve()