import sys
from bisect import bisect_left, bisect_right

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    out_lines = []
    for _ in range(T):
        N = int(data[idx]); idx += 1
        A = data[idx].decode(); idx += 1
        B = data[idx].decode(); idx += 1
        p = [i + 1 for i, c in enumerate(A) if c == '1']
        q = [i + 1 for i, c in enumerate(B) if c == '1']
        m, n = len(p), len(q)
        if m < n:
            out_lines.append("-1")
            continue
        g = [p[j + 1] - p[j] for j in range(m - 1)]

        # For each piece j: the set of targets within distance k is the
        # contiguous index interval [L_j, R_j] in target space.
        # A final configuration is a partition of pieces into n nonempty
        # contiguous groups; group t (0-based) is assigned to target q_t.
        # Constraints:
        #   (1) every piece j in group t satisfies L_j <= t <= R_j
        #       (equivalently max L over group <= t <= min R over group),
        #   (2) at the cut after piece c (between groups t and t+1),
        #       q_{t+1} - q_t <= g_c.
        # Feasibility for a given k is checked greedily: process groups in
        # order, and close each group at the LATEST valid piece.  Because all
        # constraints are "left-closed" (starting a group later never helps
        # the current group but the remaining suffix problem is monotone),
        # the latest-cut greedy is safe: if it fails, no partition exists.
        def ok(k):
            L = [0] * m
            R = [0] * m
            for j in range(m):
                L[j] = bisect_left(q, p[j] - k)
                R[j] = bisect_right(q, p[j] + k) - 1
                if L[j] > R[j]:
                    return False
            j = 0  # next unassigned piece
            for t in range(n):
                if j >= m:
                    return False
                if L[j] > t:
                    return False  # first piece of group t cannot reach it
                maxL = L[j]
                minR = R[j]
                last = -1
                jj = j
                # scan the maximal runnable group; record the latest cut
                while jj < m and L[jj] <= t:
                    if L[jj] > maxL:
                        maxL = L[jj]
                    if R[jj] < minR:
                        minR = R[jj]
                    if maxL > t or t > minR:
                        break
                    if jj == m - 1:
                        if t == n - 1:
                            last = jj
                        break
                    if t == n - 1:
                        # extra pieces cannot be appended after coverage
                        break
                    if g[jj] >= q[t + 1] - q[t]:
                        last = jj
                    jj += 1
                if last < 0:
                    return False
                j = last + 1
            return j == m

        lo, hi = 0, N
        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid):
                hi = mid
            else:
                lo = mid + 1
        out_lines.append(str(lo))
    sys.stdout.write("\n".join(out_lines) + "\n")

solve()