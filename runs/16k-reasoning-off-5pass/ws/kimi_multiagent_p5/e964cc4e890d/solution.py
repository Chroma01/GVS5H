import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    S = data[1].strip()

    # Necessary condition: first vertex black, last vertex white
    if S[0] != 'B' or S[-1] != 'W':
        print(0)
        return

    # Collect "bad cuts": prefixes [1..k] (k < 2N) with #B <= #W.
    # Cut k is uncovered iff all B_k prefix blacks are matched inside the
    # W_k prefix whites; strong connectivity needs every cut crossed.
    Ws = []
    Bs = []
    W = 0
    B = 0
    for k in range(2 * N - 1):
        if S[k] == 'W':
            W += 1
        else:
            B += 1
        if B <= W:
            Ws.append(W)
            Bs.append(B)

    m = len(Ws)
    if m == 0:
        # No constraint: every matching works.
        ans = 1
        for i in range(2, N + 1):
            ans = ans * i % MOD
        print(ans)
        return

    # Factorials / inverse factorials up to N
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Inclusion-exclusion over the chain of bad-cut events.
    #   DP_r = -W_r! - sum_{q<r} DP_q * (W_r - B_q)! / (W_q - B_q)!
    #   ans  = N! + sum_r DP_r * (N - B_r)! / (W_r - B_r)!
    # Rewrite with E_r = DP_r * invfact(W_r):
    #   E_r = -1 - sum_{q<r} E_q * fact(W_q) * fact(W_r - B_q)
    #          * invfact(W_r) * invfact(W_q - B_q)
    # Evaluate the convolution sum with a Fenwick tree keyed by B_q:
    #   sum_{q<r} A_q * fact(W_r - B_q),  A_q = E_q*fact(W_q)*invfact(W_q-B_q)
    # Fenwick node covering a range of b-values stores a polynomial P(x) so
    # that contributions A_q * fact(x - B_q) = A_q * P(x - B_q) can be
    # evaluated at x = W_r. Since fact(t) = t! we store, for each node,
    # the polynomial Q(y) = sum A_q * (y - B_q)!  ... but factorial is not
    # polynomial; instead we use the exact O(m^2) recurrence here replaced
    # by divide-and-conquer NTT below.

    # ---- Divide and conquer NTT evaluation of the recurrence ----
    # E_r depends on E_q for q < r via:
    #   E_r = -1 - invfact(W_r) * sum_{q<r} C_q * fact(W_r - B_q)
    # where C_q = E_q * fact(W_q) * invfact(W_q - B_q).
    # The sum is a convolution over the value axis: index q by B_q,
    # evaluate at W_r. We process r in order with CDQ divide and conquer,
    # using NTT to combine left-half contributions into the right half.

    # NTT implementation (mod 998244353, primitive root 3)
    def ntt(a, invert):
        n = len(a)
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j |= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        length = 2
        while length <= n:
            wlen = pow(3, (MOD - 1) // length, MOD)
            if invert:
                wlen = pow(wlen, MOD - 2, MOD)
            i = 0
            while i < n:
                w = 1
                half = length >> 1
                for j in range(i, i + half):
                    u = a[j]
                    v = a[j + half] * w % MOD
                    a[j] = (u + v) % MOD
                    a[j + half] = (u - v) % MOD
                    w = w * wlen % MOD
                i += length
            length <<= 1
        if invert:
            inv_n = pow(n, MOD - 2, MOD)
            for i in range(n):
                a[i] = a[i] * inv_n % MOD

    def convolution(a, b):
        if not a or not b:
            return []
        n = 1
        need = len(a) + len(b) - 1
        while n < need:
            n <<= 1
        fa = a + [0] * (n - len(a))
        fb = b + [0] * (n - len(b))
        ntt(fa, False)
        ntt(fb, False)
        for i in range(n):
            fa[i] = fa[i] * fb[i] % MOD
        ntt(fa, True)
        return fa[:need]

    E = [0] * m
    C = [0] * m

    # CDQ divide and conquer: compute E in order, handling cross
    # contributions from left half to right half via NTT convolution.
    # For a node [l, r): contributions of q in [l, mid) to r' in [mid, r):
    #   sum_q C_q * fact(W_{r'} - B_q)
    # Build arrays indexed by value: A[b] = sum of C_q with B_q = b
    # (b in [0..N]); kernel F[t] = fact(t). Convolution gives, at index
    # W_{r'}, the needed sum (terms with W_{r'} - B_q < 0 are excluded
    # automatically since B_q > W_{r'} would give negative index; but
    # convolution index W_{r'} sums over B_q <= W_{r'} only if we align
    # indices as A[B_q] * F[W_{r'} - B_q]; negative diffs never appear
    # because array indices are non-negative).

    sys.setrecursionlimit(1 << 25)

    def cdq(l, r):
        if r - l <= 1:
            if l < m:
                # base: E_l already has all contributions accumulated
                pass
            return
        mid = (l + r) >> 1
        cdq(l, mid)
        # contributions from [l, mid) to [mid, r)
        # A indexed by B_q value
        maxB = max(Bs[l:mid])
        maxW = max(Ws[mid:r])
        A = [0] * (maxB + 1)
        for q in range(l, mid):
            A[Bs[q]] = (A[Bs[q]] + C[q]) % MOD
        F = fact[:maxW + 1]  # F[t] = fact(t), t = W_r' - B_q >= 0
        conv = convolution(A, F)
        for rp in range(mid, r):
            w = Ws[rp]
            if w < len(conv):
                s = conv[w]
                if s:
                    E[rp] = (E[rp] - s * invfact[w]) % MOD
        cdq(mid, r)

    # Initialize E_r = -1 (the standalone term), C computed after E known.
    # But C_q depends on E_q which is finalized only after cdq on its
    # position. Standard CDQ: compute E in order; when entering cdq leaf,
    # E is final; then set C. We integrate C assignment into the recursion
    # by processing leaves in order: easiest is iterative CDQ that ensures
    # C[q] set before use. We do: cdq computes E for [l,mid) recursively
    # first (finalizing E and C there), then adds cross terms, then right.

    # We must set C inside leaves. Redefine with leaf hook.
    E = [(-1) % MOD] * m
    C = [0] * m

    def cdq2(l, r):
        if r - l == 1:
            q = l
            C[q] = E[q] * fact[Ws[q]] % MOD * invfact[Ws[q] - Bs[q]] % MOD
            return
        mid = (l + r) >> 1
        cdq2(l, mid)
        maxB = max(Bs[l:mid])
        maxW = max(Ws[mid:r])
        A = [0] * (maxB + 1)
        for q in range(l, mid):
            A[Bs[q]] = (A[Bs[q]] + C[q]) % MOD
        F = fact[:maxW + 1]
        conv = convolution(A, F)
        for rp in range(mid, r):
            w = Ws[rp]
            if w < len(conv):
                s = conv[w]
                if s:
                    E[rp] = (E[rp] - s * invfact[w]) % MOD
        cdq2(mid, r)

    cdq2(0, m)

    ans = fact[N]
    for r in range(m):
        DP_r = E[r] * fact[Ws[r]] % MOD
        ans = (ans + DP_r * fact[N - Bs[r]] % MOD * invfact[Ws[r] - Bs[r]]) % MOD

    print(ans % MOD)


main()