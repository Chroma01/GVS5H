from typing import List
import heapq
from bisect import bisect_left


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        n = len(points)
        if k <= 1 or n <= 1 or k > n:
            return 0

        two_side = 2 * side

        # chain 0: bottom + right, chain 1: left + top.
        # Corners are assigned to exactly one chain.
        arr = []
        for x, y in points:
            if y == 0:
                ch = 0
            elif x == side:
                ch = 0
            elif x == 0:
                ch = 1
            else:
                ch = 1

            u = x + y
            other = two_side - u
            h = u if u < other else other
            arr.append((u, ch, h))

        arr.sort()

        us = [0] * n
        chs = [0] * n
        hs = [0] * n
        for i, (u, ch, h) in enumerate(arr):
            us[i] = u
            chs[i] = ch
            hs[i] = h

        sorted_h = sorted(set(hs))
        m = len(sorted_h)

        # Fenwick tree over reversed h-ranks:
        # h >= threshold becomes a prefix query.
        h_to_rev = {h: m - i for i, h in enumerate(sorted_h)}
        hrev = [h_to_rev[h] for h in hs]

        # Precompute Fenwick traversal paths to reduce bit operations inside
        # the binary-search feasibility checks.
        qpaths = [()] * (m + 1)
        for q in range(1, m + 1):
            x = q
            path = []
            while x:
                path.append(x)
                x &= x - 1
            qpaths[q] = tuple(path)

        upaths = [()] * (m + 1)
        for p in range(1, m + 1):
            x = p
            path = []
            while x <= m:
                path.append(x)
                x += x & -x
            upaths[p] = tuple(path)

        upaths_idx = [upaths[hrev[i]] for i in range(n)]

        INF = 10 ** 30
        SENT = -10 ** 30

        heappush = heapq.heappush
        heappop = heapq.heappop
        bl = bisect_left

        def feasible(d: int) -> bool:
            if d == 0:
                return True

            us_l = us
            ch_l = chs
            hs_l = hs
            sh = sorted_h
            m_l = m
            n_l = n
            k_l = k
            INF_l = INF
            SENT_l = SENT
            push = heappush
            pop = heappop
            bl_l = bl
            qpaths_l = qpaths
            upaths_idx_l = upaths_idx

            # qidx[r] is the Fenwick prefix length representing active states
            # with h_i >= d - h_r.
            qidx = [0] * n_l
            for i in range(n_l):
                pos = bl_l(sh, d - hs_l[i])
                if pos < m_l:
                    qidx[i] = m_l - pos
            qpaths_idx = [qpaths_l[q] for q in qidx]
            qpaths_idx_l = qpaths_idx

            # Length 1: every point is reachable, with no relevant opposite point.
            dp = [SENT_l] * n_l
            start_idx = 0
            first_u = us_l[0]
            limit = first_u + d

            # Build lengths 2..k.
            for layer in range(1, k_l):
                if n_l - start_idx < k_l - layer:
                    return False

                ndp = [INF_l] * n_l

                heap0 = []
                heap1 = []
                tree0 = [INF_l] * (m_l + 1)
                tree1 = [INF_l] * (m_l + 1)
                min0 = INF_l
                min1 = INF_l

                first_idx = n_l

                for idx in range(start_idx, n_l):
                    u = us_l[idx]

                    # If some previous reachable state ends at least d behind,
                    # it can be extended to this and every later point, and the
                    # new state has no relevant opposite point.
                    if u >= limit:
                        if first_idx == n_l:
                            first_idx = idx
                        ndp[idx:] = [SENT_l] * (n_l - idx)
                        break

                    # Activate previous states whose stored opposite point is
                    # already d behind current u.
                    while heap0 and heap0[0][0] <= u:
                        _, i = pop(heap0)
                        ui = us_l[i]
                        if ui < min0:
                            min0 = ui
                        for pos in upaths_idx_l[i]:
                            if ui < tree0[pos]:
                                tree0[pos] = ui
                            else:
                                break

                    while heap1 and heap1[0][0] <= u:
                        _, i = pop(heap1)
                        ui = us_l[i]
                        if ui < min1:
                            min1 = ui
                        for pos in upaths_idx_l[i]:
                            if ui < tree1[pos]:
                                tree1[pos] = ui
                            else:
                                break

                    # Near transition: previous ending point must be on the
                    # opposite chain, its stored opposite point must be far
                    # enough, and cross-chain distance must be at least d.
                    q = qidx_l[idx]
                    if q:
                        if ch_l[idx] == 0:
                            if q == m_l:
                                res = min1
                            else:
                                res = INF_l
                                tree = tree1
                                for pos in qpaths_idx_l[idx]:
                                    tv = tree[pos]
                                    if tv < res:
                                        res = tv
                        else:
                            if q == m_l:
                                res = min0
                            else:
                                res = INF_l
                                tree = tree0
                                for pos in qpaths_idx_l[idx]:
                                    tv = tree[pos]
                                    if tv < res:
                                        res = tv

                        if res != INF_l:
                            ndp[idx] = res
                            if first_idx == n_l:
                                first_idx = idx

                    # Make current previous-layer state available for later points.
                    val = dp[idx]
                    if val != INF_l:
                        act = val + d
                        if act <= u:
                            ui = u
                            if ch_l[idx] == 0:
                                if ui < min0:
                                    min0 = ui
                                for pos in upaths_idx_l[idx]:
                                    if ui < tree0[pos]:
                                        tree0[pos] = ui
                                    else:
                                        break
                            else:
                                if ui < min1:
                                    min1 = ui
                                for pos in upaths_idx_l[idx]:
                                    if ui < tree1[pos]:
                                        tree1[pos] = ui
                                    else:
                                        break
                        else:
                            if ch_l[idx] == 0:
                                push(heap0, (act, idx))
                            else:
                                push(heap1, (act, idx))

                if first_idx == n_l:
                    return False

                dp = ndp
                start_idx = first_idx
                first_u = us_l[first_idx]
                limit = first_u + d

            return True

        lo = 0
        hi = two_side + 1
        while lo + 1 < hi:
            mid = (lo + hi) >> 1
            if feasible(mid):
                lo = mid
            else:
                hi = mid

        return lo