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


def main():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    if s[0] != 'B' or s[-1] != 'W':
        print(0)
        return

    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Each retained event (p, q) means:
    # all first p black vertices are paired with first q white vertices.
    # Such an event is exactly a bad prefix cut.
    events = []
    whites = 0
    blacks = 0
    pos = 0
    total_vertices = 2 * n

    while pos < total_vertices:
        if s[pos] == 'W':
            whites += 1
            pos += 1
        else:
            blacks += 1
            pos += 1

            # For this number p of black vertices, the event gets weaker
            # as q grows, so only retain the cut after its whole W-run.
            while pos < total_vertices and s[pos] == 'W':
                whites += 1
                pos += 1

            if blacks < n and whites >= blacks:
                # For equal q, the event with smallest p contains all others.
                if not events or events[-1][1] != whites:
                    events.append((blacks, whites))

    # q = N gives an unavoidable bad event.
    for _, q in events:
        if q == n:
            print(0)
            return

    k = len(events)
    if k == 0:
        print(fact[n])
        return

    ps = [p for p, _ in events]
    qs = [q for _, q in events]

    # acc[i] = q_i! + sum_{j<i} dp[j] * (q_i-p_j)!
    acc = [fact[q] for q in qs]
    dp = [0] * k

    def add_cross(l, mid, r):
        source_count = mid - l
        target_count = r - mid
        if source_count == 0 or target_count == 0:
            return

        p0 = ps[l]
        max_q = qs[r - 1]
        width = max_q - p0 + 1

        if source_count * target_count <= 5000:
            for i in range(mid, r):
                q = qs[i]
                value = 0
                for j in range(l, mid):
                    value += dp[j] * fact[q - ps[j]]
                acc[i] = (acc[i] + value) % MOD
            return

        size = 1
        while size < 2 * width - 1:
            size <<= 1

        a = [0] * size
        for j in range(l, mid):
            a[ps[j] - p0] = dp[j]

        b = [0] * size
        b[:width] = fact[:width]

        ntt(a, False)
        ntt(b, False)
        for i in range(size):
            a[i] = a[i] * b[i] % MOD
        ntt(a, True)

        for i in range(mid, r):
            acc[i] = (acc[i] + a[qs[i] - p0]) % MOD

    sys.setrecursionlimit(1_000_000)

    def cdq(l, r):
        if r - l == 1:
            gap = qs[l] - ps[l]
            dp[l] = -acc[l] * invfact[gap] % MOD
            return

        mid = (l + r) >> 1
        cdq(l, mid)
        add_cross(l, mid, r)
        cdq(mid, r)

    cdq(0, k)

    answer = fact[n]
    for i in range(k):
        answer += dp[i] * fact[n - ps[i]]

    print(answer % MOD)


if __name__ == "__main__":
    main()