import sys
from collections import deque
from itertools import combinations_with_replacement


# ======================================================================
# Exact O(N)-per-test model (validated exhaustively vs BFS for N <= 7)
# ======================================================================
#
# Pieces keep their left-to-right order (the move map x -> x +/- 1 / x is
# monotone) and coincident pieces never split, so any final configuration
# corresponds to a partition of the sorted initial positions
# p_1 < ... < p_m into r non-empty consecutive blocks, block j stacked on
# q_j, where q_1 < ... < q_r are the 1-squares of B (r <= m necessary).
#
# Let d_s = q_{j(s)} - p_s be the displacement of piece s.
#
# (1) d_1 = q_1 - p_1 and d_m = q_r - p_m are partition-INDEPENDENT (piece 1
#     is always in block 1, piece m always in block r).  Hence
#         S = d_1 - d_m = (p_m - p_1) - (q_r - q_1)
#     is fixed, and whenever the contraction constraints below hold, d is
#     non-increasing, so the bottleneck K = max_s |d_s| = max(|d_1|, |d_m|)
#     is fixed as well.
#
# Gap reductions D_t = d_t - d_{t+1} = (initial gap) - (final gap):
#   * internal gap (pieces t, t+1 in the same block): D_t = g_t >= 1 always
#     (g_t = p_{t+1} - p_t);
#   * cut gap t = s_j (boundary between blocks j and j+1):
#         D_t = g_{s_j} - h_j   (h_j = q_{j+1} - q_j),
#     so the cut is feasible iff g_{s_j} >= h_j (gaps can only contract).
#
# Operation accounting: a target strictly inside gap t shrinks it by 2
# (a_t such ops); a target on piece s shrinks the adjacent gap(s) by 1
# (b_s such ops).  Thus D_t = 2 a_t + b_t + b_{t+1}, which forces
# b_{t+1} = b_t XOR (D_t mod 2), feasible iff b_t + b_{t+1} <= D_t for all t.
#
# (4) Internal gaps never fail: g_t = 1 forces alternation (sum = 1 <= 1),
#     g_t >= 2 always works.  A cut fails only when g_{s_j} == h_j (zero
#     reduction, D_t = 0), forcing b_{s_j} = b_{s_j+1} = 0.  Since
#     b_t = b_1 XOR ((d_1 - d_t) mod 2) and d_{s_j} = q_j - p_{s_j}, this is
#         (p_{s_j} - q_j) mod 2 == (b_1 + d_1) mod 2.
#
# (2) Cost: with S = sum D_t = d_1 - d_m fixed, b_m = b_1 XOR (S mod 2), the
#     minimum number of "inward" ops is M = (S + b_1 + b_m)/2, the induced
#     net translation is u = d_1 - M + b_1, and k(b_1) = |u| + M (provably
#     minimal; boundaries never obstruct: do all inward ops first -- the
#     span only shrinks and stays inside [1, N] -- then translate).
#
# (3) So for each b_1 in {0,1} we only need: does there exist an increasing
#     cut sequence s_1 < ... < s_{r-1}, j <= s_j <= m-r+j, with
#     g_{s_j} >= h_j and the parity condition whenever g_{s_j} == h_j?
#     Validity of a candidate (t, j) is independent of the other cuts, so
#     earliest-first greedy with two pointers decides this in O(m): by
#     induction greedy's s_j stays <= the s_j of any valid solution, hence
#     greedy fails only if no solution exists.
#
# answer = min k(b_1) over the feasible b_1 in {0,1}, else -1.
# (r > m -> -1, m = 1 -> |q_1 - p_1|, and A == B -> 0 all fall out
#  naturally; no special cases needed.)


def _feasible(p, q, m, r, d1, b1):
    """Greedy existence check of a valid cut sequence for a fixed b_1."""
    if r == 1:
        return True
    want = (b1 + d1) & 1
    pos = 0  # 0-indexed candidate piece index for the next cut
    for j in range(1, r):
        lo = pos if pos > j - 1 else j - 1      # s_j >= j (1-indexed)
        hi = m - r + j - 1                      # s_j <= m - r + j
        hj = q[j] - q[j - 1]
        qj = q[j - 1]
        t = lo
        while t <= hi:
            g = p[t + 1] - p[t]
            if g > hj or (g == hj and ((p[t] - qj) & 1) == want):
                break
            t += 1
        if t > hi:
            return False
        pos = t + 1
    return True


def min_ops(p, q):
    """p, q: sorted 1-indexed positions of 1s in A and B.  Returns the
    minimum number of operations, or -1 if impossible."""
    m = len(p)
    r = len(q)
    if r > m:
        return -1
    d1 = q[0] - p[0]
    dm = q[-1] - p[-1]
    S = d1 - dm
    best = None
    for b1 in (0, 1):
        if _feasible(p, q, m, r, d1, b1):
            bm = b1 ^ (S & 1)
            M = (S + b1 + bm) // 2
            u = d1 - M + b1
            k = M + (u if u >= 0 else -u)
            if best is None or k < best:
                best = k
    return best if best is not None else -1


# ======================================================================
# Contest I/O
# ======================================================================

def solve():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        pos += 1  # N (not needed; string lengths suffice)
        A = data[pos]; pos += 1
        B = data[pos]; pos += 1
        p = [i + 1 for i, c in enumerate(A) if c == 49]
        q = [i + 1 for i, c in enumerate(B) if c == 49]
        out.append(str(min_ops(p, q)))
    sys.stdout.write("\n".join(out) + "\n")


# ======================================================================
# Built-in self-test (run with:  python solution.py --selftest)
# ======================================================================

def _ones(s):
    return [i + 1 for i, c in enumerate(s) if c == "1"]


def _str_of(mask, N):
    return "".join("1" if (mask >> i) & 1 else "0" for i in range(N))


def _bfs_answers(N):
    """Exact ground truth: ans[A_mask][B_mask] = min ops to reach a
    configuration whose support is exactly B_mask, or -1.  States are
    sorted multisets of piece positions (pieces may stack)."""
    sid = {}
    states = []
    support = []
    for sz in range(1, N + 1):
        for pos in combinations_with_replacement(range(1, N + 1), sz):
            sid[pos] = len(states)
            states.append(pos)
            mask = 0
            for x in pos:
                mask |= 1 << (x - 1)
            support.append(mask)
    S = len(states)
    trans = [None] * S
    for idx, pos in enumerate(states):
        nxt = [0] * N
        for ti in range(N):
            target = ti + 1
            np = tuple(sorted(
                x - 1 if x > target else x + 1 if x < target else x
                for x in pos))
            nxt[ti] = sid[np]
        trans[idx] = nxt
    M = 1 << N
    INF = 10 ** 9
    ans = [[-1] * M for _ in range(M)]
    for am in range(1, M):
        src = sid[tuple(i + 1 for i in range(N) if (am >> i) & 1)]
        dist = [-1] * S
        dist[src] = 0
        dq = deque([src])
        while dq:
            u = dq.popleft()
            du = dist[u] + 1
            for v in trans[u]:
                if dist[v] < 0:
                    dist[v] = du
                    dq.append(v)
        best = [INF] * M
        for u in range(S):
            d = dist[u]
            if d >= 0:
                sm = support[u]
                if d < best[sm]:
                    best[sm] = d
        row = ans[am]
        for bm in range(1, M):
            if best[bm] < INF:
                row[bm] = best[bm]
    return ans


def selftest():
    lines = []
    nfail = 0

    def check(tag, A, B, expected):
        nonlocal nfail
        got = min_ops(_ones(A), _ones(B))
        ok = got == expected
        nfail += 0 if ok else 1
        lines.append("  [%s] %-26s A=%s B=%s expected=%s got=%s"
                     % ("PASS" if ok else "FAIL", tag, A, B, expected, got))

    lines.append("== samples ==")
    check("sample 1", "01001101", "00001011", 3)
    check("sample 2", "010", "111", -1)
    check("sample 3", "10100011011110101011", "00010001111101100000", 5)

    lines.append("== edge cases ==")
    check("parity obstruction", "101101", "101010", -1)
    check("correction +1", "10011", "01011", 2)
    check("fixed extreme +1", "1101", "1110", 2)
    check("adjacent merge", "11", "10", 1)
    check("r > m", "101", "111", -1)
    check("identity (A==B)", "10110", "10110", 0)
    check("single piece", "10000", "00010", 3)
    check("r = m forced cuts", "10001", "11001", 3)
    check("gap expansion impossible", "11", "101", -1)
    check("all merge to one", "1001", "0100", 2)

    lines.append("== exhaustive BFS ground truth, all pairs N<=7 ==")
    total = 0
    mism = 0
    shown = 0
    for N in range(1, 8):
        ans = _bfs_answers(N)
        M = 1 << N
        ones_of = [None] * M
        for mask in range(1, M):
            ones_of[mask] = [i + 1 for i in range(N) if (mask >> i) & 1]
        for am in range(1, M):
            p = ones_of[am]
            row = ans[am]
            for bm in range(1, M):
                got = min_ops(p, ones_of[bm])
                total += 1
                if got != row[bm]:
                    mism += 1
                    if shown < 20:
                        lines.append(
                            "  MISMATCH N=%d A=%s B=%s brute=%d model=%d"
                            % (N, _str_of(am, N), _str_of(bm, N),
                               row[bm], got))
                        shown += 1
    lines.append("  pairs checked: %d, mismatches: %d" % (total, mism))
    nfail += mism
    lines.append("OVERALL: %s"
                 % ("ALL TESTS PASSED" if nfail == 0
                    else "%d FAILURES" % nfail))
    sys.stdout.write("\n".join(lines) + "\n")


def main():
    if "--selftest" in sys.argv:
        selftest()
        return
    solve()


if __name__ == "__main__":
    main()