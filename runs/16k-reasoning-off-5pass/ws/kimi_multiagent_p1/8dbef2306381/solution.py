import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it)); M = int(next(it)); A = int(next(it)); B = int(next(it))
    intervals = []
    for _ in range(M):
        L = int(next(it)); R = int(next(it))
        intervals.append((L, R))

    # ---- Special case: A == B (step length is forced) ----
    if A == B:
        if (N - 1) % A != 0:
            sys.stdout.write("No\n")
            return
        # visited squares: 1 + k*A for k = 0 .. (N-1)/A
        for (L, R) in intervals:
            # exists k with L <= 1 + k*A <= R ?
            lo = (L - 1 + A - 1) // A   # ceil((L-1)/A)
            hi = (R - 1) // A           # floor((R-1)/A)
            if lo <= hi:
                sys.stdout.write("No\n")
                return
        sys.stdout.write("Yes\n")
        return

    # ---- General case: A < B ----
    # Merge adjacent / touching bad intervals into maximal bad blocks
    blocks = []
    for (L, R) in intervals:
        if blocks and L <= blocks[-1][1] + 1:
            if R > blocks[-1][1]:
                blocks[-1][1] = R
        else:
            blocks.append([L, R])

    # Build gaps (nonempty free segments)
    gaps = []
    prev_end = 0  # last bad position before current gap
    for (L, R) in blocks:
        gs = prev_end + 1
        ge = L - 1
        if gs <= ge:
            gaps.append((gs, ge))
        prev_end = R
    if prev_end + 1 <= N:
        gaps.append((prev_end + 1, N))

    TH = A * A - A          # every k >= TH is a sum of values in {A, A+1}
    CAP = TH + 2 * B        # gap length beyond which "any seed => full tail"

    tail = None  # boolean list size B: reachable status of positions [ge-B+1 .. ge]

    for gi, (gs, ge) in enumerate(gaps):
        length = ge - gs + 1
        is_last = (gi == len(gaps) - 1)

        # ---- compute seeds (entry positions) within this gap ----
        if gi == 0:
            # start at square 1 (gs == 1 always here)
            seed_len = min(B, length)
            seeds = [False] * seed_len
            seeds[0] = True  # position gs == 1
        else:
            prev_gs, prev_ge = gaps[gi - 1]
            off = gs - prev_ge  # bad block length + 1 (>= 2 after merging)
            seed_len = min(B, length)
            seeds = [False] * seed_len
            dmax = min(B - off, length - 1)
            for d in range(0, dmax + 1):
                j_lo = off + d - 1
                j_hi = off + d - A + B - 1
                if j_hi > B - 1:
                    j_hi = B - 1
                if j_lo <= j_hi:
                    if any(tail[j_lo:j_hi + 1]):
                        seeds[d] = True

        any_seed = any(seeds)

        # ---- long gap: suffix beyond threshold fully reachable ----
        if length >= CAP:
            if is_last:
                sys.stdout.write("Yes\n" if any_seed else "No\n")
                return
            tail = [True] * B if any_seed else [False] * B
            continue

        # ---- short gap: sliding-window DP ----
        reach = [False] * length
        wsum = 0
        for p in range(length):
            pa = p - A
            if pa >= 0 and reach[pa]:
                wsum += 1
            pb = p - B - 1
            if pb >= 0 and reach[pb]:
                wsum -= 1
            s = seeds[p] if p < len(seeds) else False
            reach[p] = s or (wsum > 0)

        if is_last:
            sys.stdout.write("Yes\n" if reach[length - 1] else "No\n")
            return

        # extract tail: positions ge-B+1 .. ge
        tail = [False] * B
        base = length - B
        for j in range(B):
            idx = base + j
            if idx >= 0 and reach[idx]:
                tail[j] = True

    # Should not reach here (last gap always returns), but just in case
    sys.stdout.write("No\n")

solve()