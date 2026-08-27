import sys

MOD = 998244353


def build_factors(maxv):
    spf = list(range(maxv + 1))
    if maxv >= 1:
        spf[1] = 1
    r = int(maxv ** 0.5)
    for i in range(2, r + 1):
        if spf[i] == i:
            for j in range(i * i, maxv + 1, i):
                if spf[j] == j:
                    spf[j] = i

    factors = [[] for _ in range(maxv + 1)]
    for x in range(2, maxv + 1):
        y = x
        while y > 1:
            p = spf[y]
            e = 0
            while y % p == 0:
                y //= p
                e += 1
            factors[x].append((p, e))
    return factors


def scale_dp(dp, lo, hi, L, p, powp, mod=MOD):
    if L == 0 or lo > hi:
        return
    if L == 1:
        pp = powp
        for h in range(lo, hi + 1):
            dp[h] = (dp[h] * pp[h]) % mod
    else:
        base = pow(p, L, mod)
        scale = pow(base, lo, mod)
        for h in range(lo, hi + 1):
            dp[h] = (dp[h] * scale) % mod
            scale = (scale * base) % mod


def general_both(l, r, oldT, oldM, pp, nT, nM, aa, TT, mod=MOD):
    for j in range(l, r):
        pt = pp[j]

        vt = 0
        if j >= aa:
            vt = oldT[j - aa]
        if j + aa <= TT:
            vt += oldT[j + aa]
        nT[j] = (vt * pt) % mod

        vm = 0
        if j >= aa:
            vm = oldM[j - aa]
        if j + aa < TT:
            vm += oldM[j + aa]
        nM[j] = (vm * pt) % mod


def fast_both(l, r, oldT, oldM, pp, nT, nM, aa, mod=MOD):
    for j in range(l, r):
        vt = oldT[j - aa] + oldT[j + aa]
        nT[j] = (vt * pp[j]) % mod
        vm = oldM[j - aa] + oldM[j + aa]
        nM[j] = (vm * pp[j]) % mod


def general_T(l, r, oldT, pp, nT, aa, TT, mod=MOD):
    for j in range(l, r):
        vt = 0
        if j >= aa:
            vt = oldT[j - aa]
        if j + aa <= TT:
            vt += oldT[j + aa]
        nT[j] = (vt * pp[j]) % mod


def fast_T(l, r, oldT, pp, nT, aa, mod=MOD):
    for j in range(l, r):
        vt = oldT[j - aa] + oldT[j + aa]
        nT[j] = (vt * pp[j]) % mod


def general_M(l, r, oldM, pp, nM, aa, TT, mod=MOD):
    for j in range(l, r):
        vm = 0
        if j >= aa:
            vm = oldM[j - aa]
        if j + aa < TT:
            vm += oldM[j + aa]
        nM[j] = (vm * pp[j]) % mod


def fast_M(l, r, oldM, pp, nM, aa, mod=MOD):
    for j in range(l, r):
        vm = oldM[j - aa] + oldM[j + aa]
        nM[j] = (vm * pp[j]) % mod


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:1 + N - 1]
    maxv = max(A) if A else 1

    factors = build_factors(maxv)
    events = [[] for _ in range(maxv + 1)]
    totals = [0] * (maxv + 1)

    for idx, x in enumerate(A):
        for p, e in factors[x]:
            events[p].append((idx, e))
            totals[p] += e

    ans = 1
    mod = MOD

    for p in range(2, maxv + 1):
        T = totals[p]
        if T == 0:
            continue

        ev = events[p]

        powp = [1] * (T + 1)
        for h in range(1, T + 1):
            powp[h] = (powp[h - 1] * p) % mod

        # DP for G_T
        dpT = powp[:]
        loT, hiT = 0, T
        deadT = False

        # DP for G_{T-1}
        if T >= 1:
            dpM = powp[:T]
            loM, hiM = 0, T - 1
            deadM = False
        else:
            dpM = []
            loM, hiM = 1, 0
            deadM = True

        pos = 0

        for idx, a in ev:
            L = idx - pos
            if L:
                if not deadT:
                    scale_dp(dpT, loT, hiT, L, p, powp)
                if not deadM:
                    scale_dp(dpM, loM, hiM, L, p, powp)

            # New bounding box for G_T
            if deadT:
                nloT, nhiT = T + 1, -1
            else:
                H = T
                nloT = H + 1
                nhiT = -1
                limit = H - a

                if loT <= limit:
                    up_lo = loT + a
                    up_hi = (hiT if hiT < limit else limit) + a
                    if up_lo < nloT:
                        nloT = up_lo
                    if up_hi > nhiT:
                        nhiT = up_hi

                if hiT >= a:
                    down_lo = (loT if loT > a else a) - a
                    down_hi = hiT - a
                    if down_lo < nloT:
                        nloT = down_lo
                    if down_hi > nhiT:
                        nhiT = down_hi

            # New bounding box for G_{T-1}
            if T >= 1 and not deadM:
                Hm = T - 1
                nloM = Hm + 1
                nhiM = -1
                limit = Hm - a

                if loM <= limit:
                    up_lo = loM + a
                    up_hi = (hiM if hiM < limit else limit) + a
                    if up_lo < nloM:
                        nloM = up_lo
                    if up_hi > nhiM:
                        nhiM = up_hi

                if hiM >= a:
                    down_lo = (loM if loM > a else a) - a
                    down_hi = hiM - a
                    if down_lo < nloM:
                        nloM = down_lo
                    if down_hi > nhiM:
                        nhiM = down_hi
            else:
                nloM, nhiM = T, -1

            deadT_new = nloT > nhiT
            deadM_new = (T < 1) or (nloM > nhiM)

            newT = [0] * (T + 1) if not deadT_new else None
            newM = [0] * T if not deadM_new else None

            if not deadT_new or not deadM_new:
                oldT = dpT
                oldM = dpM
                pp = powp
                aa = a
                TT = T
                nT = newT
                nM = newM

                if not deadT_new and not deadM_new:
                    l = nloT if nloT < nloM else nloM
                    r = (nhiT if nhiT > nhiM else nhiM) + 1
                elif not deadT_new:
                    l = nloT
                    r = nhiT + 1
                else:
                    l = nloM
                    r = nhiM + 1

                while l < r:
                    inT = (not deadT_new) and (nloT <= l <= nhiT)
                    inM = (not deadM_new) and (nloM <= l <= nhiM)

                    nxt = r
                    if inT:
                        b = nhiT + 1
                        if b < nxt:
                            nxt = b
                    else:
                        if l < nloT:
                            b = nloT
                            if b < nxt:
                                nxt = b

                    if inM:
                        b = nhiM + 1
                        if b < nxt:
                            nxt = b
                    else:
                        if l < nloM:
                            b = nloM
                            if b < nxt:
                                nxt = b

                    if nxt <= l:
                        nxt = l + 1

                    if inT and inM:
                        end = nxt
                        if TT >= 2 * aa:
                            if l < aa:
                                e = aa if aa < end else end
                                general_both(l, e, oldT, oldM, pp, nT, nM, aa, TT)

                            s = aa if aa > l else l
                            e = TT - aa
                            if e > end:
                                e = end
                            if s < e:
                                fast_both(s, e, oldT, oldM, pp, nT, nM, aa)

                            s = TT - aa
                            if s < l:
                                s = l
                            if s < end:
                                general_both(s, end, oldT, oldM, pp, nT, nM, aa, TT)
                        else:
                            general_both(l, end, oldT, oldM, pp, nT, nM, aa, TT)

                    elif inT:
                        end = nxt
                        if TT >= 2 * aa:
                            if l < aa:
                                e = aa if aa < end else end
                                general_T(l, e, oldT, pp, nT, aa, TT)

                            s = aa if aa > l else l
                            e = TT - aa + 1
                            if e > end:
                                e = end
                            if s < e:
                                fast_T(s, e, oldT, pp, nT, aa)

                            s = TT - aa + 1
                            if s < l:
                                s = l
                            if s < end:
                                general_T(s, end, oldT, pp, nT, aa, TT)
                        else:
                            general_T(l, end, oldT, pp, nT, aa, TT)

                    elif inM:
                        end = nxt
                        if TT >= 2 * aa + 1:
                            if l < aa:
                                e = aa if aa < end else end
                                general_M(l, e, oldM, pp, nM, aa, TT)

                            s = aa if aa > l else l
                            e = TT - aa
                            if e > end:
                                e = end
                            if s < e:
                                fast_M(s, e, oldM, pp, nM, aa)

                            s = TT - aa
                            if s < l:
                                s = l
                            if s < end:
                                general_M(s, end, oldM, pp, nM, aa, TT)
                        else:
                            general_M(l, end, oldM, pp, nM, aa, TT)

                    l = nxt

            dpT = newT if not deadT_new else []
            dpM = newM if not deadM_new else []
            loT, hiT = nloT, nhiT
            loM, hiM = nloM, nhiM
            deadT = deadT_new
            deadM = deadM_new
            pos = idx + 1

        L = (N - 1) - pos
        if L:
            if not deadT:
                scale_dp(dpT, loT, hiT, L, p, powp)
            if not deadM:
                scale_dp(dpM, loM, hiM, L, p, powp)

        GT = sum(dpT[loT:hiT + 1]) % mod if not deadT else 0
        GM = sum(dpM[loM:hiM + 1]) % mod if not deadM else 0

        F = (GT - pow(p, N, mod) * GM) % mod
        ans = (ans * F) % mod

        if ans == 0:
            break

    print(ans)


if __name__ == "__main__":
    main()