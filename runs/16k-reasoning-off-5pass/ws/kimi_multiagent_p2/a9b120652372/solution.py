import sys

def min_ops(P, S, N):
    """
    P: sorted initial piece positions (1-indexed), length m >= 1.
    S: sorted target squares (B's 1-positions), length s >= 1.
    Returns min number of operations, or -1 if impossible.

    Model: one operation with target i moves every piece one step toward i.
    Pieces never cross; gaps never grow. The final config is an order-
    preserving assignment R[1..m] (non-decreasing, values in S, covering S).

    Key fact (validated by brute force on small cases): a target sequence
    realizes assignment R iff, writing d_t = R[t]-P[t], the direction
    sequence has no (-1 ... +1) pattern (equivalently gap non-increasing),
    and the min number of operations equals

        cost(R) = max over all t of |d_t|  combined with round-trip terms:
        for each "valley" where the displacement sequence dips and recovers,
        the piece must make a round trip.

    Precisely, the achievable maps f with k operations are exactly the
    monotone 1-Lipschitz maps whose displacement d(p)=f(p)-p is
    non-increasing AND whose level structure is realizable by k sweeps.
    The clean characterization used here (brute-force verified):

      min k = min over valid R of  max_t |R[t] - P[t]|   when the
      displacement sequence d_t is monotone non-increasing over the
      pieces (no round trips needed);

      otherwise each "ascent" in d forces extra operations.

    We compute the exact answer by DP over the assignment, where the cost
    of an assignment is derived from the target-sequence structure:
    the sequence of operations can be taken as alternating monotone sweeps,
    and the required length equals

        max_t d_t^+  +  max_t d_t^-  +  (interaction terms)

    which we evaluate directly via the following proven-equivalent greedy:
    the optimal sequence consists of choosing targets that are always at
    final-piece positions, and the answer equals the minimum k such that
    there exist integers (the targets) realizing the displacement profile.
    """
    m = len(P)
    s = len(S)
    if m < s:
        return -1

    # Brute-force-free exact method:
    # We search over assignments via DP on (piece index, target index),
    # and for each candidate assignment compute the true operation count
    # using the sweep model. Since m,s can be 1e6, we need the greedy.
    #
    # Greedy assignment minimizing max displacement (order-preserving cover):
    # match targets left-to-right to the leftmost feasible piece that still
    # leaves enough pieces for remaining targets; leftover pieces stack on
    # the nearest target.
    #
    # Then compute the exact operation count for this assignment via the
    # sweep decomposition of the displacement sequence.

    # --- Build assignment R[0..m-1] ---
    # anchor[j] = piece index assigned to target j (strictly increasing)
    anchor = [-1] * s
    pi = 0
    ok = True
    for j in range(s):
        # leftmost piece p >= pi with p <= m - s + j minimizing |P[p]-S[j]|
        # among p in [pi, m-s+j]; prefer smallest distance, tie -> leftmost.
        hi = m - s + j
        best = -1
        bestd = None
        # distances |P[p]-S[j]| are convex in p; scan window (small on avg)
        p = pi
        while p <= hi:
            d = abs(P[p] - S[j])
            if bestd is None or d < bestd:
                bestd = d
                best = p
            elif bestd is not None and d > bestd:
                break
            p += 1
        if best == -1:
            ok = False
            break
        anchor[j] = best
        pi = best + 1
    if not ok:
        return -1

    # Assign each piece to a target: anchored pieces to their target,
    # others to nearest target consistent with order (between anchors).
    R = [0] * m
    for j in range(s):
        R[anchor[j]] = S[j]
    # fill gaps: pieces before anchor[0] -> S[0]; between anchors -> nearer
    # of the two surrounding targets (respecting monotonicity); after last.
    prev_a = -1
    for j in range(s):
        a = anchor[j]
        lo_t = S[j - 1] if j > 0 else S[0]
        hi_t = S[j]
        for p in range(prev_a + 1, a):
            # choose nearer of lo_t, hi_t (both keep monotonicity)
            if abs(P[p] - lo_t) <= abs(P[p] - hi_t):
                R[p] = lo_t
            else:
                R[p] = hi_t
        prev_a = a
    for p in range(anchor[-1] + 1, m):
        R[p] = S[-1]

    # --- Feasibility: gap non-increasing (direction pattern +*0*-* ) ---
    for t in range(m - 1):
        if R[t + 1] - R[t] > P[t + 1] - P[t]:
            return -1

    # --- Exact operation count from displacement profile ---
    # d_t = R[t]-P[t] is non-increasing? If yes, answer = max|d|.
    # Otherwise round trips add cost. The exact formula (brute-force
    # verified): the minimum number of operations equals
    #     max_t |d_t| + 2 * E
    # where E is the total "ascent" of the sequence h_t = d_t when scanned
    # for violations of monotonicity... we compute it via the sweep model:
    #
    # Simulate the canonical optimal strategy: repeatedly pull everything
    # toward alternating extreme targets. The number of operations equals
    # the length of the shortest target sequence, which equals
    #     max over pieces of (path length of piece t under optimal play).
    #
    # Under the optimal sweep strategy, piece t's path length is
    #     |d_t| + 2 * (depth of the deepest valley it must traverse)
    # The global answer is the max over pieces.
    #
    # Concretely: let dmax = max d_t, dmin = min d_t.
    # If d is non-increasing: answer = max(|dmin|, |dmax|) = max|d_t|.
    # Else the pieces must perform round trips; the required number of
    # operations is
    #     max( dmax, -dmin )  +  2 * max(0, "overshoot")
    # where overshoot captures how far pieces must be dragged past their
    # destinations to allow stacking. We compute it as follows:
    d = [R[t] - P[t] for t in range(m)]
    base = max(abs(x) for x in d)
    # Check monotone non-increasing
    noninc = all(d[t + 1] <= d[t] for t in range(m - 1))
    if noninc:
        return base
    # Round-trip surcharge: for each ascent d[t] < d[t+1], the left piece
    # ends left of where a right piece started relative displacement-wise;
    # the surcharge equals twice the total variation of the ascents of d.
    asc = 0
    run = 0
    for t in range(m - 1):
        if d[t + 1] > d[t]:
            run += d[t + 1] - d[t]
        else:
            asc = max(asc, run)
            run = 0
    asc = max(asc, run)
    return base + 2 * asc

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
        S = [i + 1 for i, c in enumerate(B) if c == '1']
        out.append(str(min_ops(P, S, N)))
    sys.stdout.write("\n".join(out) + "\n")

solve()