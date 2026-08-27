import sys
from bisect import bisect_left, bisect_right
import heapq

INF = 10**18


def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    answers = []

    for _ in range(t):
        n = int(next(it))
        a = next(it)
        b = next(it)

        x = [i for i, c in enumerate(a) if c == 49]
        y = [i for i, c in enumerate(b) if c == 49]
        p = len(x)
        q = len(y)

        if p < q:
            answers.append("-1")
            continue

        # Ignore distances and parity.  This checks whether the necessary
        # non-expansion condition can ever be satisfied.
        def structurally_possible():
            if q == 1:
                return True

            pos = 0
            for s in range(q - 1):
                need = y[s + 1] - y[s]
                while pos < p - 1 and x[pos + 1] - x[pos] < need:
                    pos += 1
                if pos >= p - 1:
                    return False
                pos += 1
            return True

        if not structurally_possible():
            answers.append("-1")
            continue

        pref_odd_x = [0] * (p + 1)
        for i, v in enumerate(x):
            pref_odd_x[i + 1] = pref_odd_x[i] + (v & 1)

        # Number of sources among x[0:cnt] whose parity differs from target.
        def mismatch_prefix(target, cnt):
            odd_sources = pref_odd_x[cnt]
            if target & 1:
                return cnt - odd_sources
            return odd_sources

        def feasible(k):
            L = [0] * q
            R = [0] * q

            for s, target in enumerate(y):
                lo = bisect_left(x, target - k)
                hi = bisect_right(x, target + k) - 1
                if lo > hi:
                    return False
                L[s] = lo
                R[s] = hi

            # The leftmost / rightmost source must be assigned respectively
            # to the leftmost / rightmost target.
            if L[0] != 0 or R[-1] != p - 1:
                return False

            if q == 1:
                odd = mismatch_prefix(y[0], p)
                if k & 1:
                    return p - odd <= k
                return odd <= k

            # A boundary r after target 0 simultaneously has to satisfy
            # target 0's right endpoint and target 1's left endpoint.
            lo0 = max(L[0], L[1] - 1, 0)
            hi0 = min(R[0], R[1] - 1, p - q)
            if lo0 > hi0:
                return False

            prev_lo = lo0
            prev_hi = hi0
            prev_min = [
                mismatch_prefix(y[0], r + 1)
                for r in range(prev_lo, prev_hi + 1)
            ]
            prev_max = prev_min[:]

            # DP over block boundaries.  For each feasible boundary, retain
            # the minimum and maximum possible number of odd displacements.
            for s in range(1, q - 1):
                cur_lo = max(L[s], L[s + 1] - 1, s)
                cur_hi = min(R[s], R[s + 1] - 1, p - q + s)
                if cur_lo > cur_hi:
                    return False

                needed_gap = y[s] - y[s - 1]

                min_heap = []
                max_heap = []
                add = prev_lo

                cur_min = [INF] * (cur_hi - cur_lo + 1)
                cur_max = [-INF] * (cur_hi - cur_lo + 1)

                for r in range(cur_lo, cur_hi + 1):
                    limit = min(r - 1, prev_hi)

                    while add <= limit:
                        if x[add + 1] - x[add] >= needed_gap:
                            idx = add - prev_lo
                            base = mismatch_prefix(y[s], add + 1)
                            heapq.heappush(min_heap, prev_min[idx] - base)
                            heapq.heappush(max_heap, base - prev_max[idx])
                        add += 1

                    if min_heap:
                        end = mismatch_prefix(y[s], r + 1)
                        idx = r - cur_lo
                        cur_min[idx] = end + min_heap[0]
                        cur_max[idx] = end - max_heap[0]

                prev_lo, prev_hi = cur_lo, cur_hi
                prev_min, prev_max = cur_min, cur_max

            needed_gap = y[-1] - y[-2]
            min_odd = INF
            max_odd = -INF

            for r in range(prev_lo, prev_hi + 1):
                if x[r + 1] - x[r] < needed_gap:
                    continue

                idx = r - prev_lo
                if prev_min[idx] == INF:
                    continue

                suffix = (
                    mismatch_prefix(y[-1], p)
                    - mismatch_prefix(y[-1], r + 1)
                )

                min_odd = min(min_odd, prev_min[idx] + suffix)
                max_odd = max(max_odd, prev_max[idx] + suffix)

            if min_odd == INF:
                return False

            if k & 1:
                return p - max_odd <= k
            return min_odd <= k

        best = INF

        # Feasibility is monotone among operation counts of the same parity.
        for parity in (0, 1):
            lo = parity
            hi = n if (n & 1) == parity else n + 1

            while lo < hi:
                mid = (lo + hi) // 2
                if (mid & 1) != parity:
                    mid -= 1
                if mid < lo:
                    mid += 2

                if feasible(mid):
                    hi = mid
                else:
                    lo = mid + 2

            if feasible(lo):
                best = min(best, lo)

        answers.append(str(best if best != INF else -1))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()