import sys

def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        A = data[idx].decode(); idx += 1
        B = data[idx].decode(); idx += 1

        a_pos = [i + 1 for i, c in enumerate(A) if c == '1']
        b_pos = [i + 1 for i, c in enumerate(B) if c == '1']
        m = len(a_pos)
        g = len(b_pos)

        if m < g:
            out.append("-1")
            continue

        # Decision: is there an order-preserving surjective partition of the
        # m pieces into g consecutive groups (group k -> b_k) such that
        #   (b) |s_j - b_{kappa(j)}| <= K for every piece j
        #   (a) b_{k+1} - b_k <= s_{j+1} - s_j at each group boundary (j last
        #       piece of group k, j+1 first piece of group k+1)
        # By the constructive sweep argument (see NOTES) this is exactly
        # reachability in <= K operations.
        def feasible(K):
            # Greedy leftmost partition: repeatedly take the SHORTEST prefix
            # of remaining pieces for the current target b_k such that the
            # boundary gap condition to the next piece can hold, while never
            # taking a piece out of range and never leaving fewer pieces than
            # remaining targets.
            j = 0  # first unassigned piece
            for k in range(g):
                remaining_targets = g - k - 1
                # last piece index we may take for this group:
                #   must leave >= remaining_targets pieces
                max_take = m - remaining_targets - 1  # inclusive index bound
                # pieces must satisfy |s - b_k| <= K
                lo = b_pos[k] - K
                hi = b_pos[k] + K
                # first piece of group is j; it must be in range
                if not (lo <= a_pos[j] <= hi):
                    return False
                # extend the group as far as allowed by range and count
                r = j
                while (r + 1 <= max_take) and (lo <= a_pos[r + 1] <= hi):
                    r += 1
                # Now choose the actual end e of this group in [j, r].
                # If k < g-1 we need the boundary gap condition:
                #   a_pos[e+1] - a_pos[e] >= b_pos[k+1] - b_pos[k]
                # Pick the SMALLEST e satisfying it (leave as many pieces as
                # possible for later groups); if none works, fail.
                if k < g - 1:
                    need = b_pos[k + 1] - b_pos[k]
                    e = -1
                    for cand in range(j, r + 1):
                        if a_pos[cand + 1] - a_pos[cand] >= need:
                            e = cand
                            break
                    if e == -1:
                        return False
                    j = e + 1
                else:
                    # last group must consume all remaining pieces
                    if r != m - 1:
                        return False
                    j = m
            return j == m

        # Binary search minimum K (answer is at most N)
        lo, hi = 0, n
        if not feasible(hi):
            out.append("-1")
            continue
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        out.append(str(lo))

    sys.stdout.write("\n".join(out) + "\n")

solve()