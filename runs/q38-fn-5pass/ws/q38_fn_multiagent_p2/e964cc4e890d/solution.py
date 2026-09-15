import sys

MOD = 998244353
G = 3


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1]

    # Necessary endpoint conditions.
    if S[0] != 66 or S[-1] != 87:  # 'B', 'W'
        print(0)
        return

    # Generate compressed prefix constraints.
    # For the (b+1)-th black vertex, b = number of previous blacks,
    # w = number of previous whites.  If w >= b, we need
    # max(first b permutation values) > w.
    # If w is the same as a previous kept constraint, the later one is redundant.
    j_arr = []
    a_arr = []
    w = 0
    b = 0
    last_a = -1

    for ch in S:
        if ch == 66:  # 'B'
            if b >= 1 and w >= b and w > last_a:
                j_arr.append(b)
                a_arr.append(w)
                last_a = w
            b += 1
        else:
            w += 1

    M = len(j_arr)
    mod = MOD

    if M == 0:
        ans = 1
        for i in range(2, N + 1):
            ans = ans * i % mod
        print(ans)
        return

    maxM = a_arr[-1] - j_arr[0]
    maxL = 1 << (maxM.bit_length())
    max_fact = max(N, maxL)

    fact = [1] * (max_fact + 1)
    for i in range(1, max_fact + 1):
        fact[i] = fact[i - 1] * i % mod

    invfact = [1] * (max_fact + 1)
    invfact[max_fact] = pow(fact[max_fact], mod - 2, mod)
    for i in range(max_fact, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod

    F = [0] * M
    acc = [0] * M

    ff = fact
    iv = invfact
    jj = j_arr
    aa = a_arr
    FF = F
    ac = acc

    # Small cases are faster with direct O(M^2) DP.
    SMALL = 3000
    if M <= SMALL:
        for i in range(M):
            ai = aa[i]
            s = 0
            for p in range(i):
                s += FF[p] * ff[ai - jj[p]]
            FF[i] = ((ff[ai] - s) % mod) * iv[ai - jj[i]] % mod
    else:
        max_log = maxL.bit_length() - 1

        # Precompute NTT roots.
        roots_f = [None] * (max_log + 1)
        roots_i = [None] * (max_log + 1)

        for log in range(1, max_log + 1):
            half = 1 << (log - 1)
            wlen = pow(G, (mod - 1) >> log, mod)
            arr = [1] * half
            for i in range(1, half):
                arr[i] = arr[i - 1] * wlen % mod
            roots_f[log] = arr

            inv_arr = [1] * half
            for i in range(1, half):
                inv_arr[i] = mod - arr[half - i]
            roots_i[log] = inv_arr

        inv_len = [1] * (max_log + 1)
        inv2 = (mod + 1) // 2
        for log in range(1, max_log + 1):
            inv_len[log] = inv_len[log - 1] * inv2 % mod

        # Forward NTT: DIF, output is bit-reversed.
        def ntt(a, roots=roots_f, mod=mod):
            n = len(a)
            log = n.bit_length() - 1
            while log:
                half = 1 << (log - 1)
                length = half << 1
                rts = roots[log]
                for start in range(0, n, length):
                    for j in range(half):
                        i = start + j
                        k = i + half
                        u = a[i]
                        v = a[k]
                        x = u + v
                        if x >= mod:
                            x -= mod
                        y = u - v
                        if y < 0:
                            y += mod
                        a[i] = x
                        a[k] = y * rts[j] % mod
                log -= 1

        # Inverse NTT: DIT, input is bit-reversed, output is natural.
        def intt(a, roots=roots_i, inv_len=inv_len, mod=mod):
            n = len(a)
            maxlog = n.bit_length() - 1
            log = 1
            while log <= maxlog:
                half = 1 << (log - 1)
                length = half << 1
                rts = roots[log]
                for start in range(0, n, length):
                    for j in range(half):
                        i = start + j
                        k = i + half
                        u = a[i]
                        v = a[k] * rts[j] % mod
                        x = u + v
                        if x >= mod:
                            x -= mod
                        y = u - v
                        if y < 0:
                            y += mod
                        a[i] = x
                        a[k] = y
                log += 1

            inv_n = inv_len[maxlog]
            for i in range(n):
                a[i] = a[i] * inv_n % mod

        kernel_cache = {}

        def get_kernel(log, fact=fact, ntt=ntt, cache=kernel_cache):
            arr = cache.get(log)
            if arr is None:
                L = 1 << log
                arr = fact[:L]
                ntt(arr)
                cache[log] = arr
            return arr

        def add_ntt(
            l,
            mid,
            r,
            jj=jj,
            aa=aa,
            FF=FF,
            ac=ac,
            mod=mod,
            ntt=ntt,
            intt=intt,
            get_kernel=get_kernel,
        ):
            min_x = jj[l]
            max_y = aa[r - 1]
            span = max_y - min_x
            log = span.bit_length()
            L = 1 << log

            U = [0] * L
            for p in range(l, mid):
                U[jj[p] - min_x] = FF[p]

            ntt(U)
            Khat = get_kernel(log)
            for i in range(L):
                U[i] = U[i] * Khat[i] % mod
            intt(U)

            for t in range(mid, r):
                ac[t] += U[aa[t] - min_x]

        def add_naive(l, mid, r, ff=ff, jj=jj, aa=aa, FF=FF, ac=ac):
            pl = range(l, mid)
            for t in range(mid, r):
                at = aa[t]
                s = 0
                for p in pl:
                    s += FF[p] * ff[at - jj[p]]
                ac[t] += s

        LEAF = 64
        CROSS_LIMIT = 32768
        sys.setrecursionlimit(1_000_000)

        def solve(l, r, ff=ff, jj=jj, aa=aa, FF=FF, ac=ac, iv=iv, mod=mod):
            if r - l <= LEAF:
                for i in range(l, r):
                    ai = aa[i]
                    s = ac[i]
                    for p in range(l, i):
                        s += FF[p] * ff[ai - jj[p]]
                    FF[i] = ((ff[ai] - s) % mod) * iv[ai - jj[i]] % mod
                return

            mid = (l + r) // 2
            solve(l, mid)

            if (mid - l) * (r - mid) <= CROSS_LIMIT:
                add_naive(l, mid, r)
            else:
                add_ntt(l, mid, r)

            solve(mid, r)

        solve(0, M)

    ans = fact[N]
    s = 0
    for i in range(M):
        s += FF[i] * fact[N - jj[i]]

    print((ans - s) % mod)


if __name__ == "__main__":
    main()