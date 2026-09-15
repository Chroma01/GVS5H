import sys

MOD = 998244353


def calc_prime(p, dlist, mod):
    H = sum(dlist)
    if H == 0:
        return 1

    # pw[h] = p^h mod mod
    pw = [1] * (H + 1)
    for i in range(1, H + 1):
        pw[i] = (pw[i - 1] * p) % mod

    # total[h]: sum of weights of prefixes ending at height h,
    #           regardless of whether height 0 has been visited.
    # zero[h]:  same, but only prefixes that have already visited height 0.
    total = pw[:]
    zero = [0] * (H + 1)
    zero[0] = 1

    for d in dlist:
        if d == 0:
            # Height does not change; add current height to the exponent sum.
            total = [(t * w) % mod for t, w in zip(total, pw)]
            zero = [(z * w) % mod for z, w in zip(zero, pw)]
            continue

        ntotal = [0] * (H + 1)
        nzero = [0] * (H + 1)

        # Target height 0 can only be reached from height d.
        # Any path reaching 0 becomes "seen zero".
        v = total[d]
        ntotal[0] = v
        nzero[0] = v

        tot = total
        zer = zero
        pw_local = pw
        H_local = H
        d_local = d
        L = H_local - d_local

        # For target height nh > 0, sources are nh-d and nh+d.
        # Split into ranges to avoid per-iteration boundary checks.
        if d_local <= L:
            # Only source nh+d exists.
            for nh in range(1, d_local):
                h = nh + d_local
                w = pw_local[nh]
                ntotal[nh] = (tot[h] * w) % mod
                nzero[nh] = (zer[h] * w) % mod

            # Both sources exist.
            for nh in range(d_local, L + 1):
                h1 = nh - d_local
                h2 = nh + d_local
                st = tot[h1] + tot[h2]
                sz = zer[h1] + zer[h2]
                if st >= mod:
                    st -= mod
                if sz >= mod:
                    sz -= mod
                w = pw_local[nh]
                ntotal[nh] = (st * w) % mod
                nzero[nh] = (sz * w) % mod

            # Only source nh-d exists.
            for nh in range(L + 1, H_local + 1):
                h = nh - d_local
                w = pw_local[nh]
                ntotal[nh] = (tot[h] * w) % mod
                nzero[nh] = (zer[h] * w) % mod
        else:
            # Only source nh+d exists.
            for nh in range(1, L + 1):
                h = nh + d_local
                w = pw_local[nh]
                ntotal[nh] = (tot[h] * w) % mod
                nzero[nh] = (zer[h] * w) % mod

            # Heights L+1 .. d-1 are unreachable for this step.

            # Only source nh-d exists.
            for nh in range(d_local, H_local + 1):
                h = nh - d_local
                w = pw_local[nh]
                ntotal[nh] = (tot[h] * w) % mod
                nzero[nh] = (zer[h] * w) % mod

        total = ntotal
        zero = nzero

    return sum(zero) % mod


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    M = N - 1
    A = data[1:1 + M]

    maxA = max(A) if A else 1

    # Smallest prime factor sieve up to max(A).
    spf = list(range(maxA + 1))
    if maxA >= 1:
        spf[1] = 1
    for i in range(2, int(maxA ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, maxA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # For each prime, store v_p(A_i) for all i.
    prime_exps = {}
    for idx, a in enumerate(A):
        x = a
        while x > 1:
            p = spf[x]
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            if p not in prime_exps:
                prime_exps[p] = [0] * M
            prime_exps[p][idx] = cnt

    ans = 1
    for p, dlist in prime_exps.items():
        ans = (ans * calc_prime(p, dlist, MOD)) % MOD

    print(ans)


if __name__ == "__main__":
    main()