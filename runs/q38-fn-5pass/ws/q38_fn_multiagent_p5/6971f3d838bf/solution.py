from typing import List
from array import array


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0

        # Original maximum subarray sum (no deletion).
        cur = best = nums[0]
        occ = {}

        for i, v in enumerate(nums):
            if i:
                if cur < 0:
                    cur = v
                else:
                    cur += v
                if cur > best:
                    best = cur

            # Only negative values can improve the answer.
            if v < 0:
                lst = occ.get(v)
                if lst is None:
                    occ[v] = [i]
                else:
                    lst.append(i)

        if not occ:
            return best

        # If the only negative candidate is the whole array, deletion is invalid.
        if all(len(pos) == n for pos in occ.values()):
            return best

        # Safe sentinel: |sum| <= 1e11, and -1e18 fits in signed 64-bit arrays.
        NEG = -10**18

        # Prefix statistics for intervals [0, i).
        pt = array('q', [0]) * (n + 1)
        pp = array('q', [NEG]) * (n + 1)
        ps = array('q', [NEG]) * (n + 1)
        pb = array('q', [NEG]) * (n + 1)

        ct, cp, cs, cb = 0, NEG, NEG, NEG
        for i, v in enumerate(nums):
            # Merge current prefix with leaf (v, v, v, v).
            total = ct + v

            x = ct + v
            pref = cp if cp >= x else x

            x = v + cs
            suff = v if v >= x else x

            x = cs + v
            best_val = cb if cb >= v else v
            if x > best_val:
                best_val = x

            ct, cp, cs, cb = total, pref, suff, best_val
            pt[i + 1] = ct
            pp[i + 1] = cp
            ps[i + 1] = cs
            pb[i + 1] = cb

        # Suffix statistics for intervals [i, n).
        st = array('q', [0]) * (n + 1)
        sp = array('q', [NEG]) * (n + 1)
        ss = array('q', [NEG]) * (n + 1)
        sb = array('q', [NEG]) * (n + 1)

        ct, cp, cs, cb = 0, NEG, NEG, NEG
        for i in range(n - 1, -1, -1):
            v = nums[i]
            # Merge leaf (v, v, v, v) with current suffix.
            total = v + ct

            x = v + cp
            pref = v if v >= x else x

            x = ct + v
            suff = cs if cs >= x else x

            x = v + cp
            best_val = v if v >= cb else cb
            if x > best_val:
                best_val = x

            ct, cp, cs, cb = total, pref, suff, best_val
            st[i] = ct
            sp[i] = cp
            ss[i] = cs
            sb[i] = cb

        # Segment tree is only needed for middle gaps between consecutive occurrences.
        need_tree = False
        for pos in occ.values():
            if len(pos) >= 2:
                need_tree = True
                break

        if need_tree:
            size = 1
            while size < n:
                size <<= 1
            base = size

            # Lists are faster for the heavily queried tree; prefix/suffix use arrays for memory.
            tt = [0] * (2 * size)
            tp = [NEG] * (2 * size)
            ts = [NEG] * (2 * size)
            tb = [NEG] * (2 * size)

            for i, v in enumerate(nums):
                idx = base + i
                tt[idx] = v
                tp[idx] = v
                ts[idx] = v
                tb[idx] = v

            for i in range(base - 1, 0, -1):
                li = i << 1
                ri = li | 1

                ta, pa, sa, ba = tt[li], tp[li], ts[li], tb[li]
                tbv, pbv, sbv, bbv = tt[ri], tp[ri], ts[ri], tb[ri]

                total = ta + tbv

                x = ta + pbv
                pref = pa if pa >= x else x

                x = tbv + sa
                suff = sbv if sbv >= x else x

                x = sa + pbv
                best_val = ba if ba >= bbv else bbv
                if x > best_val:
                    best_val = x

                tt[i] = total
                tp[i] = pref
                ts[i] = suff
                tb[i] = best_val

            def query(l, r, tt=tt, tp=tp, ts=ts, tb=tb, base=base, NEG=NEG):
                l += base
                r += base

                lt, lp, ls, lb = 0, NEG, NEG, NEG
                rt, rp, rs, rb = 0, NEG, NEG, NEG

                while l < r:
                    if l & 1:
                        nt, np, ns, nb = tt[l], tp[l], ts[l], tb[l]

                        total = lt + nt

                        x = lt + np
                        pref = lp if lp >= x else x

                        x = nt + ls
                        suff = ns if ns >= x else x

                        x = ls + np
                        best_val = lb if lb >= nb else nb
                        if x > best_val:
                            best_val = x

                        lt, lp, ls, lb = total, pref, suff, best_val
                        l += 1

                    if r & 1:
                        r -= 1
                        nt, np, ns, nb = tt[r], tp[r], ts[r], tb[r]

                        total = nt + rt

                        x = nt + rp
                        pref = np if np >= x else x

                        x = rt + ns
                        suff = rs if rs >= x else x

                        x = ns + rp
                        best_val = nb if nb >= rb else rb
                        if x > best_val:
                            best_val = x

                        rt, rp, rs, rb = total, pref, suff, best_val

                    l >>= 1
                    r >>= 1

                total = lt + rt

                x = lt + rp
                pref = lp if lp >= x else x

                x = rt + ls
                suff = rs if rs >= x else x

                x = ls + rp
                best_val = lb if lb >= rb else rb
                if x > best_val:
                    best_val = x

                return total, pref, suff, best_val
        else:
            def query(l, r):
                return 0, NEG, NEG, NEG

        ans = best

        for pos in occ.values():
            m = len(pos)
            if m == n:
                continue

            has = False
            mt = mp = ms = mb = 0

            # First gap: [0, pos[0])
            first = pos[0]
            if pb[first] != NEG:
                mt, mp, ms, mb = pt[first], pp[first], ps[first], pb[first]
                has = True

            prev = first + 1

            # Middle gaps: (pos[j-1], pos[j])
            for j in range(1, m):
                p = pos[j]
                if prev < p:
                    nt, np, ns, nb = query(prev, p)

                    if not has:
                        mt, mp, ms, mb = nt, np, ns, nb
                        has = True
                    else:
                        total = mt + nt

                        x = mt + np
                        pref = mp if mp >= x else x

                        x = nt + ms
                        suff = ns if ns >= x else x

                        x = ms + np
                        best_val = mb if mb >= nb else nb
                        if x > best_val:
                            best_val = x

                        mt, mp, ms, mb = total, pref, suff, best_val

                prev = p + 1

            # Last gap: [last + 1, n)
            if sb[prev] != NEG:
                nt, np, ns, nb = st[prev], sp[prev], ss[prev], sb[prev]

                if not has:
                    mt, mp, ms, mb = nt, np, ns, nb
                    has = True
                else:
                    total = mt + nt

                    x = mt + np
                    pref = mp if mp >= x else x

                    x = nt + ms
                    suff = ns if ns >= x else x

                    x = ms + np
                    best_val = mb if mb >= nb else nb
                    if x > best_val:
                        best_val = x

                    mt, mp, ms, mb = total, pref, suff, best_val

            if has and mb > ans:
                ans = mb

        return ans