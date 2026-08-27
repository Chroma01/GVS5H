from typing import List
from functools import lru_cache
import bisect


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        lo, hi = 0, max(points) * (m + 1)
        ans = 0
        while lo <= hi:
            mid = (lo + hi) >> 1
            if self._min_moves(points, mid) <= m:
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans

    # Minimum number of moves so that every gameScore[i] >= X.
    #
    # Model: let v[i] = ceil(X / points[i]) (required visits to index i).
    # Let x_i = number of crossings of edge (i-1, i) (edge 0 is the entry
    # from -1 to 0).  Total moves = sum x_i, and with end position e:
    #   * x_i >= 1,  x_i odd iff e >= i   (parity constraint)
    #   * x_i + x_{i+1} >= 2*v[i] - [e == i],  x_n = 0
    # For fixed e the right-to-left greedy is optimal.  Indices right of e
    # use even parity (one suffix precompute).  Indices left of e are only
    # ever queried at odd inputs t, where the odd-parity rounding vanishes:
    # x_i(t) = max(1, 2*v[i] - t) exactly.  So each prefix function is a
    # composition of clamps h_i(t) = max(1, D_i - t), represented as a
    # piecewise-linear breakpoint list and combined in a segment tree.
    def _min_moves(self, points: List[int], X: int) -> int:
        n = len(points)
        v = [(X + p - 1) // p for p in points]
        D = [2 * vv for vv in v]

        # suffix-even greedy pass (right to left): sx[i], ssum[i]
        sx = [0] * (n + 1)
        ssum = [0] * (n + 1)
        x_next = 0
        run = 0
        for i in range(n - 1, -1, -1):
            need = D[i] - x_next
            val = need if need > 2 else 2
            if val & 1:
                val += 1
            sx[i] = val
            run += val
            ssum[i] = run
            x_next = val

        # candidate (odd) value x_e for each end position e
        q_t = [0] * n
        for e in range(n):
            xe = D[e] - 1 - sx[e + 1]
            if xe < 1:
                xe = 1
            q_t[e] = xe

        NEG = -(1 << 62)

        # Piecewise function representation: list of segments
        # (t0, x0, s0, k) meaning for t in [t0, next_t0):
        #   x(t) = x0 - (t - t0)          (slope -1)
        #   s(t) = s0 - k * (t - t0)      (cumulative sum, integer slope k)
        # Segments are ordered by increasing t0; x decreases as t grows.

        def evalF(F, t):
            lo, hi = 0, len(F)
            while lo < hi:
                mid = (lo + hi) >> 1
                if F[mid][0] <= t:
                    lo = mid + 1
                else:
                    hi = mid
            t0, x0, s0, k = F[lo - 1]
            dt = t - t0
            return x0 - dt, s0 - k * dt

        def compose(A, B):
            # (A ∘ B)(t): B applied first (higher indices), then A.
            res = []
            astarts = [a[0] for a in A]
            nb = len(B)
            for bi in range(nb):
                t0, x0, s0, kb = B[bi]
                t1 = B[bi + 1][0] if bi + 1 < nb else None
                x_end = NEG if t1 is None else x0 - (t1 - t0)
                lo_i = bisect.bisect_right(astarts, x_end)
                hi_i = bisect.bisect_right(astarts, x0) - 1
                cur_t = t0
                cur_x = x0
                ai = hi_i
                while ai >= lo_i:
                    a_t0, a_x0, a_s0, ka = A[ai]
                    x_stop = a_t0 if a_t0 > x_end else x_end
                    dt = cur_x - a_t0
                    ax = a_x0 - dt
                    asum = a_s0 - ka * dt
                    res.append((cur_t, ax,
                                s0 - kb * (cur_t - t0) + asum,
                                kb + ka))
                    adv = cur_x - x_stop
                    cur_t += adv
                    cur_x = x_stop
                    if x_stop == x_end:
                        break
                    ai -= 1
            # merge adjacent collinear segments to keep lists compact
            merged = []
            for seg in res:
                if merged:
                    pt, px, ps, pk = merged[-1]
                    t0, x0, s0, k = seg
                    dt = t0 - pt
                    if pk == k and px - dt == x0 and ps - pk * dt == s0:
                        continue
                merged.append(seg)
            return merged

        tree = [None] * (4 * n)

        def build(node, lo, hi):
            if lo == hi:
                Di = D[lo]
                tree[node] = [(NEG, Di, Di, 1), (Di - 1, 1, 1, 0)]
                return
            mid = (lo + hi) >> 1
            build(node << 1, lo, mid)
            build(node << 1 | 1, mid + 1, hi)
            tree[node] = compose(tree[node << 1], tree[node << 1 | 1])

        build(1, 0, n - 1)

        def query_prefix(e, t):
            # cumulative sum of x_0..x_{e-1} with input t at edge e
            if e == 0:
                return 0
            nodes = []
            stack = [(1, 0, n - 1)]
            while stack:
                nd, l, r = stack.pop()
                if r > e - 1:
                    mid = (l + r) >> 1
                    stack.append((nd << 1, l, mid))
                    stack.append((nd << 1 | 1, mid + 1, r))
                else:
                    nodes.append((l, nd))
            nodes.sort(key=lambda z: -z[0])  # right-to-left order
            total = 0
            cur = t
            for l, nd in nodes:
                x_out, s_out = evalF(tree[nd], cur)
                total += s_out
                cur = x_out
            return total

        best = None
        for e in range(n):
            s = ssum[e + 1] + q_t[e] + query_prefix(e, q_t[e])
            if best is None or s < best:
                best = s
        return best