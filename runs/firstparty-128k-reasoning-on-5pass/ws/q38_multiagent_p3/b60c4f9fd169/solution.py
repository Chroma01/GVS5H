import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    K = int(data[0]); S = data[1]; T = data[2]
    n0, m0 = len(S), len(T)
    if abs(n0 - m0) > K:
        print('No'); return

    i = 0; lim = min(n0, m0)
    while i < lim and S[i] == T[i]:
        i += 1
    j = 0; lim = min(n0 - i, m0 - i)
    while j < lim and S[n0 - 1 - j] == T[m0 - 1 - j]:
        j += 1

    S = S[i:n0 - j]; T = T[i:m0 - j]
    n, m = len(S), len(T)

    if n == 0 and m == 0:
        print('Yes'); return
    if n == 0 or m == 0:
        print('Yes' if abs(n - m) <= K else 'No'); return

    cache = {}; CH = 8192

    def lcp(x, y):
        if x < 0 or y < 0 or x >= n or y >= m:
            return 0
        key = (x, y)
        if key in cache:
            return cache[key]

        max_l = min(n - x, m - y); l = 0
        ss = S; tt = T; ch = CH

        while max_l >= ch:
            b = tt[y:y + ch]
            if ss.startswith(b, x):
                x += ch; y += ch; l += ch; max_l -= ch
            else:
                a = ss[x:x + ch]
                z = int.from_bytes(a, 'little') ^ int.from_bytes(b, 'little')
                l += ((z & -z).bit_length() - 1) // 8
                cache[key] = l; return l

        if max_l:
            b = tt[y:y + max_l]
            if ss.startswith(b, x):
                l += max_l
            else:
                a = ss[x:x + max_l]
                z = int.from_bytes(a, 'little') ^ int.from_bytes(b, 'little')
                l += ((z & -z).bit_length() - 1) // 8

        cache[key] = l; return l

    size = 2 * K + 1; off = K; dp = [-1] * size
    dp[off] = lcp(0, 0)
    if dp[off] == n and dp[off] == m:
        print('Yes'); return

    for e in range(1, K + 1):
        ndp = [-1] * size
        for d in range(-e, e + 1):
            best = -1

            idx = off + d
            if 0 <= idx < size:
                v = dp[idx]
                if v >= 0 and v < n and 0 <= v + d < m:
                    best = v + 1

            idx = off + d - 1
            if 0 <= idx < size:
                v = dp[idx]
                if v >= 0 and 0 <= v + d - 1 < m and v > best:
                    best = v

            idx = off + d + 1
            if 0 <= idx < size:
                v = dp[idx]
                if v >= 0 and v < n and 0 <= v + d + 1 <= m:
                    cand = v + 1
                    if cand > best:
                        best = cand

            if best >= 0:
                y = best + d
                if best < n and 0 <= y < m:
                    best += lcp(best, y)
                ndp[off + d] = best
                if best == n and best + d == m:
                    print('Yes'); return
        dp = ndp

    print('No')

if __name__ == '__main__':
    solve()