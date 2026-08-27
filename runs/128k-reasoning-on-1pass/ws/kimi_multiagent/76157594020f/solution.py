from collections import deque

class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        a = [1 if c == '1' else 0 for c in s]

        # Fast edge: no flips -> answer is the current longest run.
        if numOps == 0:
            best = 1
            cur = 1
            for i in range(1, n):
                if a[i] == a[i - 1]:
                    cur += 1
                    if cur > best:
                        best = cur
                else:
                    cur = 1
            return best
        # Fast edge: enough flips to force a fully alternating string.
        if numOps >= n:
            return 1

        def min_flips(L: int) -> int:
            """
            Minimum flips to make every run of identical bits have length <= L.

            Let g[i][b] = min flips for prefix s[0..i] where the final run
            (containing i) consists of bit b. If the final run is s[j+1..i]
            (length i-j <= L), then:
                g[i][b] = min over j in [i-L, i-1] of
                          g[j][1-b] + (i-j) - (P_b[i] - P_b[j])
            with g[-1][*] = 0, P_b[-1] = 0 (P_b = prefix count of bit b).

            Using P_0[j] + P_1[j] = j+1 and defining Q_b[j] = g[j][b] - P_b[j],
            this simplifies to:
                g[i][b] = (i - P_b[i]) + 1 + min Q_{1-b}[j]  over the window,
            where Q_{1-b}[-1] = 0 acts as sentinel (block covers whole prefix).
            The sliding window minimum is maintained with a monotonic deque,
            giving an O(n) check. Indices are shifted by +1 so shifted index 0
            represents j = -1.
            """
            Q0 = [0] * (n + 1)
            Q1 = [0] * (n + 1)
            dq0 = deque([0])  # sentinel j = -1
            dq1 = deque([0])
            P0 = P1 = 0
            g0 = g1 = 0
            for i in range(n):
                if a[i] == 0:
                    P0 += 1
                else:
                    P1 += 1
                lo = i - L + 1  # smallest allowed shifted index (j = i - L)
                while dq0[0] < lo:
                    dq0.popleft()
                while dq1[0] < lo:
                    dq1.popleft()
                g0 = (i - P0) + 1 + Q1[dq1[0]]
                g1 = (i - P1) + 1 + Q0[dq0[0]]
                q0 = g0 - P0
                q1 = g1 - P1
                Q0[i + 1] = q0
                Q1[i + 1] = q1
                while Q0[dq0[-1]] >= q0:
                    dq0.pop()
                dq0.append(i + 1)
                while Q1[dq1[-1]] >= q1:
                    dq1.pop()
                dq1.append(i + 1)
            return g0 if g0 < g1 else g1

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if min_flips(mid) <= numOps:
                hi = mid
            else:
                lo = mid + 1
        return lo