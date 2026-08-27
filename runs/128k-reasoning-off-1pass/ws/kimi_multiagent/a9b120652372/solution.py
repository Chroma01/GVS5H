import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    out = []
    for _ in range(T):
        N = int(data[idx]); idx += 1
        A = data[idx].decode(); idx += 1
        B = data[idx].decode(); idx += 1
        P = [i + 1 for i, c in enumerate(A) if c == '1']
        Q = [i + 1 for i, c in enumerate(B) if c == '1']
        m, t = len(P), len(Q)
        if m < t:
            out.append("-1")
            continue

        # Feasibility for a given k:
        #  - order-preserving matching: g[s] = piece index matched to target s,
        #    greedy leftmost-available with |P[g[s]] - Q[s]| <= k.
        #  - every unmatched piece must be absorbable into an adjacent matched
        #    target without crossing (gap check).
        #  - separability: scanning pieces left to right, once we have seen a
        #    piece that must move LEFT (assigned target < position), no later
        #    piece may need to move RIGHT (assigned target > position).
        #    (In one operation all right-movers must lie left of the pivot and
        #    all left-movers right of it; under a monotone assignment this
        #    prefix/suffix structure is preserved at every step, so the
        #    condition on the initial assignment is necessary and sufficient.)
        def check(k):
            g = [-1] * t
            j = 0
            for s in range(t):
                qs = Q[s]
                while j < m and P[j] < qs - k:
                    j += 1
                if j < m and P[j] <= qs + k:
                    g[s] = j
                    j += 1
                else:
                    return False
            # absorption + separability in one left-to-right sweep
            seen_left = False  # have we seen a piece needing to move left?
            prev = -1
            for s in range(t):
                cur = g[s]
                qs = Q[s]
                lo_b = qs - k
                hi_b = qs + k
                # unmatched pieces strictly between g[s-1] and g[s]
                for jj in range(prev + 1, cur):
                    p = P[jj]
                    # may end at Q[s-1] or Q[s] (only Q[0] if s == 0)
                    if lo_b <= p <= hi_b:
                        tgt = qs
                    elif s > 0 and Q[s-1] - k <= p <= Q[s-1] + k:
                        tgt = Q[s-1]
                    else:
                        return False
                    if p < tgt:            # must move right
                        if seen_left:
                            return False
                    elif p > tgt:          # must move left
                        seen_left = True
                # matched piece g[s] -> Q[s]
                p = P[cur]
                if p < qs:
                    if seen_left:
                        return False
                elif p > qs:
                    seen_left = True
                prev = cur
            # unmatched pieces after g[t-1] must end at Q[t-1]
            qt = Q[t-1]
            for jj in range(prev + 1, m):
                p = P[jj]
                if not (qt - k <= p <= qt + k):
                    return False
                if p < qt:
                    if seen_left:
                        return False
                elif p > qt:
                    seen_left = True
            return True

        hi = N
        if not check(hi):
            out.append("-1")
            continue
        lo = 0
        while lo < hi:
            mid = (lo + hi) // 2
            if check(mid):
                hi = mid
            else:
                lo = mid + 1
        out.append(str(lo))
    sys.stdout.write("\n".join(out) + "\n")

solve()