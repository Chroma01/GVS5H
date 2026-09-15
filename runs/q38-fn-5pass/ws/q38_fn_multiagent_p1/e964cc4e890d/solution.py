import sys

MOD = 998244353
G = 3


def main():
    input = sys.stdin.readline
    N = int(input())
    S = input().strip()

    # Necessary conditions for any strongly connected matching.
    if S[0] != 'B' or S[-1] != 'W':
        print(0)
        return

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    # Build reduced constraints.
    # For the (s+1)-th black vertex, R_s = number of whites before it.
    # Keep only first increases of R_s with R_s >= s.
    s_arr = []
    r_arr = []
    last_R = -1
    whites = 0
    blacks = 0

    for ch in S:
        if ch == 'W':
            whites += 1
        else:
            blacks += 1
            if blacks >= 2:
                s = blacks - 1
                r = whites
                if r > last_R:
                    last_R = r
                    if r >= s:
                        s_arr.append(s)
                        r_arr.append(r)

    m = len(s_arr)

    # No nontrivial prefix constraints: every matching is valid.
    if m == 0:
        print(fact[N] % MOD)
        return

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Small cases: direct O(m^2) DP.
    if m <= 2000:
        add = [0] * m
        D = [0] * m
        for i in range(m):
            ri = r_arr[i]
            val = MOD - fact[ri] - add[i]
            if val < 0:
                val += MOD
            if val >= MOD:
                val -= MOD
            D[i] = val * invfact[ri - s_arr[i]] % MOD

            di = D[i]
            if di:
                si = s_arr[i]
                for j in range(i + 1, m):
                    prod = di * fact[r_arr[j] - si] % MOD
                    nv = add[j] + prod
                    if nv >= MOD:
                        nv -= MOD
                    add[j] = nv

        ans = fact[N]
        for i in range(m):
            ans = (ans + D[i] * fact[N - s_arr[i]]) % MOD
        print(ans)
        return

    # NTT roots.
    max_len = 1
    while max_len < 2 * N + 5:
        max_len <<= 1
    MAXLOG = max_len.bit_length() - 1

    roots_f = [0] * (MAXLOG + 1)
    roots_i = [0] * (MAXLOG + 1)
    inv_len = [0] * (MAXLOG + 1)

    inv2 = (MOD + 1) // 2
    inv_len[0] = 1
    for k in range(1, MAXLOG + 1):
        L = 1 << k
        roots_f[k] = pow(G, (MOD - 1) // L, MOD)
        roots_i[k] = pow(roots_f[k], MOD - 2, MOD)
        inv_len[k] = inv_len[k - 1] * inv2 % MOD

    # Forward NTT: decimation-in-frequency, output is bit-reversed.
    def ntt(a):
        n = len(a)
        mod = MOD
        length = n
        stage = n.bit_length() - 1
        roots = roots_f

        while length > 1:
            half = length >> 1
            wlen = roots[stage]
            for i in range(0, n, length):
                w = 1
                end = i + half
                for j in range(i, end):
                    u = a[j]
                    v = a[j + half]

                    x = u + v
                    if x >= mod:
                        x -= mod

                    y = u - v
                    if y < 0:
                        y += mod

                    a[j] = x
                    a[j + half] = (y * w) % mod
                    w = (w * wlen) % mod

            length = half
            stage -= 1

    # Inverse NTT: decimation-in-time, input is bit-reversed.
    def intt(a):
        n = len(a)
        mod = MOD
        length = 2
        stage = 1
        roots = roots_i

        while length <= n:
            half = length >> 1
            wlen = roots[stage]
            for i in range(0, n, length):
                w = 1
                end = i + half
                for j in range(i, end):
                    u = a[j]
                    v = a[j + half] * w % mod

                    x = u + v
                    if x >= mod:
                        x -= mod

                    y = u - v
                    if y < 0:
                        y += mod

                    a[j] = x
                    a[j + half] = y
                    w = (w * wlen) % mod

            length <<= 1
            stage += 1

        inv_n = inv_len[n.bit_length() - 1]
        for i in range(n):
            a[i] = a[i] * inv_n % mod

    add = [0] * m
    D = [0] * m

    BLOCK = 64
    CROSS_LIMIT = 8000

    def naive_add(l, mid, r):
        for i in range(l, mid):
            di = D[i]
            if di == 0:
                continue
            si = s_arr[i]
            for j in range(mid, r):
                prod = di * fact[r_arr[j] - si] % MOD
                nv = add[j] + prod
                if nv >= MOD:
                    nv -= MOD
                add[j] = nv

    def convolve_add(l, mid, r):
        s_min = s_arr[l]
        s_max_left = s_arr[mid - 1]
        len_a = s_max_left - s_min + 1

        r_min_right = r_arr[mid]
        r_max_right = r_arr[r - 1]
        len_b = (r_max_right - r_min_right) + len_a

        min_d = r_min_right - s_max_left
        total = len_a + len_b - 1
        n = 1 << (total - 1).bit_length()

        fa = [0] * n
        fb = [0] * n

        for idx in range(l, mid):
            fa[s_arr[idx] - s_min] = D[idx]

        fb[:len_b] = fact[min_d:min_d + len_b]

        ntt(fa)
        ntt(fb)

        mod = MOD
        for i in range(n):
            fa[i] = fa[i] * fb[i] % mod

        intt(fa)

        base = s_min + min_d
        for j in range(mid, r):
            q = r_arr[j] - base
            val = fa[q]
            if val:
                nv = add[j] + val
                if nv >= MOD:
                    nv -= MOD
                add[j] = nv

    sys.setrecursionlimit(1_000_000)

    def solve(l, r):
        if r - l <= BLOCK:
            for i in range(l, r):
                ri = r_arr[i]
                val = MOD - fact[ri] - add[i]
                if val < 0:
                    val += MOD
                if val >= MOD:
                    val -= MOD

                D[i] = val * invfact[ri - s_arr[i]] % MOD

                di = D[i]
                if di:
                    si = s_arr[i]
                    for j in range(i + 1, r):
                        prod = di * fact[r_arr[j] - si] % MOD
                        nv = add[j] + prod
                        if nv >= MOD:
                            nv -= MOD
                        add[j] = nv
            return

        mid = (l + r) // 2
        solve(l, mid)

        prod = (mid - l) * (r - mid)
        if prod <= CROSS_LIMIT:
            naive_add(l, mid, r)
        else:
            # If the coordinate span is unusually large compared with the
            # number of pairs, naive addition is often faster.
            len_a_est = s_arr[mid - 1] - s_arr[l] + 1
            len_b_est = (r_arr[r - 1] - r_arr[mid]) + len_a_est
            total_est = len_a_est + len_b_est - 1
            ntt_est = 1 << (total_est - 1).bit_length()

            if ntt_est > 4 * prod:
                naive_add(l, mid, r)
            else:
                convolve_add(l, mid, r)

        solve(mid, r)

    solve(0, m)

    ans = fact[N]
    for i in range(m):
        ans = (ans + D[i] * fact[N - s_arr[i]]) % MOD

    print(ans)


if __name__ == "__main__":
    main()