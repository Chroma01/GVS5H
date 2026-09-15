from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if n == 0:
            return 0
        if n == 1:
            return points[0] if m >= 1 else 0
        if m < n:
            return 0

        cap = m + 1
        base0 = 2 * n - 1
        max_p = max(points)
        min_p = min(points)

        def feasible(
            x: int,
            pts=points,
            nn=n,
            mm=m,
            cp=cap,
            base=base0,
            mn=min_p,
        ) -> bool:
            # Visiting every index once is always possible when m >= n.
            if x <= mn:
                return True

            # a[i] = residual demand if i is before the final index.
            # b[i] = residual demand if i is in the returned suffix.
            a = [0] * nn
            b = [0] * nn

            for i, p in enumerate(pts):
                ci = (x + p - 1) // p

                ai = ci - 1
                if ai < 0:
                    ai = 0
                if ai > cp:
                    ai = cp
                a[i] = ai

                if i == nn - 1:
                    b[i] = ai
                else:
                    bi = ci - 2
                    if bi < 0:
                        bi = 0
                    if bi > cp:
                        bi = cp
                    b[i] = bi

            # Suffix maximum-weight independent set DP over b[i..n-1].
            # suf1[i]: best when i is selected, suf0[i]: best when i is not selected.
            suf0 = [0] * nn
            suf1 = [0] * nn
            suf1[nn - 1] = b[nn - 1]

            for i in range(nn - 2, -1, -1):
                v1 = b[i] + suf0[i + 1]
                if v1 > cp:
                    v1 = cp
                suf1[i] = v1

                v0 = suf0[i + 1]
                if suf1[i + 1] > v0:
                    v0 = suf1[i + 1]
                suf0[i] = v0

            # Final index E = 0: residual weights are b[0..n-1].
            mwis = suf0[0] if suf0[0] >= suf1[0] else suf1[0]
            if base + 2 * mwis <= mm:
                return True

            # Sweep final index E = 1..n-1.
            # Prefix MWIS states over a[0..E-1].
            pref0 = 0
            pref1 = a[0]

            for E in range(1, nn):
                # Residual weights are a[0..E-1] + b[E..n-1].
                s_any = suf0[E] if suf0[E] >= suf1[E] else suf1[E]

                # If prefix last (E-1) is selected, suffix first (E) cannot be selected.
                mwis = pref0 + s_any
                alt = pref1 + suf0[E]
                if alt > mwis:
                    mwis = alt
                if mwis > cp:
                    mwis = cp

                # Skeleton moves for final index E:
                # -1 -> n-1 -> E, total 2n - 1 - E.
                if base - E + 2 * mwis <= mm:
                    return True

                # Add a[E] to the prefix for the next final index E + 1.
                if E < nn - 1:
                    new_pref1 = pref0 + a[E]
                    if new_pref1 > cp:
                        new_pref1 = cp
                    new_pref0 = pref0 if pref0 >= pref1 else pref1
                    pref0, pref1 = new_pref0, new_pref1

            return False

        # Total score is at most max(points) * m, so the minimum score is
        # at most floor(max(points) * m / n).
        lo = min_p
        hi = max_p * m // n
        if hi < lo:
            hi = lo

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo

    # Development-only brute-force validator for tiny cases.
    # It is intentionally not called by maxScore.
    def _brute_feasible(self, points: List[int], m: int, x: int) -> bool:
        if x == 0:
            return True

        n = len(points)
        if n == 0:
            return False

        req = [(x + p - 1) // p for p in points]

        if m < n:
            return False
        if sum(req) > m:
            return False

        start_visits = [0] * n
        start_visits[0] = 1
        start_state = (0, tuple(start_visits))

        queue = [start_state]
        seen = {start_state}
        moves = 1

        if all(start_visits[i] >= req[i] for i in range(n)):
            return True

        while queue and moves < m:
            nxt = []
            for pos, visits in queue:
                for npos in (pos - 1, pos + 1):
                    if 0 <= npos < n:
                        if visits[npos] < req[npos]:
                            tmp = list(visits)
                            tmp[npos] += 1
                            nvisits = tuple(tmp)
                        else:
                            nvisits = visits

                        state = (npos, nvisits)
                        if state not in seen:
                            if all(nvisits[i] >= req[i] for i in range(n)):
                                return True
                            seen.add(state)
                            nxt.append(state)

            queue = nxt
            moves += 1

        return False