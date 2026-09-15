import sys
from math import isqrt

MOD = 998244353


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:]
    m = N - 1

    maxA = max(A) if A else 1
    spf = list(range(maxA + 1))
    if maxA >= 1:
        spf[1] = 1
    for i in range(2, isqrt(maxA) + 1):
        if spf[i] == i:
            for j in range(i * i, maxA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    exps = {}
    for idx, x in enumerate(A):
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            if p not in exps:
                exps[p] = [0] * m
            exps[p][idx] = e

    ans = 1
    mod = MOD

    for p, a_list in exps.items():
        H = sum(a_list)

        pw = [1] * (H + 1)
        for i in range(1, H + 1):
            pw[i] = (pw[i - 1] * p) % mod

        seen = [0] * (H + 1)
        seen[0] = 1

        unseen = pw[:]
        unseen[0] = 0

        pref = 0
        suffix = H

        for a in a_list:
            new_pref = pref + a
            new_suffix = suffix - a

            ns = [0] * (H + 1)
            nu = [0] * (H + 1)

            if a == 0:
                for h in range(pref + 1):
                    v = seen[h]
                    if v:
                        ns[h] = (v * pw[h]) % mod

                for h in range(1, suffix + 1):
                    v = unseen[h]
                    if v:
                        nu[h] = (v * pw[h]) % mod

            else:
                # Transition for states that have already seen a zero.
                for nh in range(new_pref + 1):
                    val = 0

                    if nh >= a:
                        val += seen[nh - a]
                    if nh + a <= pref:
                        val += seen[nh + a]
                    if nh == 0:
                        val += unseen[a]

                    if val:
                        if val >= mod:
                            val -= mod
                        if val >= mod:
                            val -= mod
                        ns[nh] = (val * pw[nh]) % mod

                # Transition for states that have not seen a zero yet.
                for nh in range(1, new_suffix + 1):
                    val = 0

                    if nh > a:
                        val += unseen[nh - a]
                    if nh + a <= suffix:
                        val += unseen[nh + a]

                    if val:
                        if val >= mod:
                            val -= mod
                        if val >= mod:
                            val -= mod
                        nu[nh] = (val * pw[nh]) % mod

            seen, unseen = ns, nu
            pref, suffix = new_pref, new_suffix

        ans = (ans * (sum(seen) % mod)) % mod

    print(ans)


if __name__ == "__main__":
    solve()