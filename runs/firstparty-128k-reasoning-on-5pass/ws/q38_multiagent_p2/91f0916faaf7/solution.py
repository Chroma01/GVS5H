import sys
from math import isqrt

MOD = 998244353


def contribution(a_list, p, H):
    mod = MOD
    HH = H
    HH1 = HH + 1

    # pp[h] = p^h mod mod
    pp = [1] * HH1
    for i in range(1, HH1):
        pp[i] = (pp[i - 1] * p) % mod

    # total[h]: all walks with heights in [0, H] ending at h
    # miss[h]:  walks with all heights > 0 ending at h
    total = pp[:]
    miss = [0] + pp[1:]

    for a in a_list:
        if a == 0:
            tot = total
            mis = miss
            for h in range(1, HH1):
                ph = pp[h]
                tot[h] = (tot[h] * ph) % mod
                mis[h] = (mis[h] * ph) % mod
        else:
            t = total
            m = miss
            nt = [0] * HH1
            nm = [0] * HH1

            # new height 0 can only come from old height a
            nt[0] = t[a]

            ha = HH - a

            # h where only h+a is a valid predecessor
            up_end = a - 1
            if up_end > ha:
                up_end = ha
            for h in range(1, up_end + 1):
                ph = pp[h]
                hp = h + a
                nt[h] = (t[hp] * ph) % mod
                nm[h] = (m[hp] * ph) % mod

            # h where both h+a and h-a are valid predecessors
            both_start = a
            both_end = ha
            if both_start <= both_end:
                for h in range(both_start, both_end + 1):
                    ph = pp[h]
                    hp = h + a
                    hm = h - a

                    s = t[hp] + t[hm]
                    if s >= mod:
                        s -= mod
                    nt[h] = (s * ph) % mod

                    ms = m[hp] + m[hm]
                    if ms >= mod:
                        ms -= mod
                    nm[h] = (ms * ph) % mod

            # h where only h-a is a valid predecessor
            down_start = ha + 1
            if down_start < a:
                down_start = a
            for h in range(down_start, HH1):
                ph = pp[h]
                hm = h - a
                nt[h] = (t[hm] * ph) % mod
                nm[h] = (m[hm] * ph) % mod

            total = nt
            miss = nm

    return (sum(total) - sum(miss)) % mod


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:1 + N - 1]
    maxA = max(A) if A else 1

    # smallest prime factor up to maxA
    spf = list(range(maxA + 1))
    if maxA >= 1:
        spf[1] = 1
    for i in range(2, isqrt(maxA) + 1):
        if spf[i] == i:
            for j in range(i * i, maxA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # precompute factorization of every possible A_i
    factors = [[] for _ in range(maxA + 1)]
    for x in range(2, maxA + 1):
        y = x
        while y > 1:
            p = spf[y]
            e = 0
            while y % p == 0:
                y //= p
                e += 1
            factors[x].append((p, e))

    m = N - 1
    vals = {}

    for i, x in enumerate(A):
        for p, e in factors[x]:
            lst = vals.get(p)
            if lst is None:
                lst = [0] * m
                vals[p] = lst
            lst[i] = e

    ans = 1
    for p, a_list in vals.items():
        H = sum(a_list)
        if H == 0:
            continue
        ans = (ans * contribution(a_list, p, H)) % MOD

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()