import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    A = int(data[idx]); idx += 1
    B = int(data[idx]); idx += 1
    intervals = []
    for _ in range(M):
        L = int(data[idx]); idx += 1
        R = int(data[idx]); idx += 1
        intervals.append((L, R))

    # mask: bit k (0-indexed) = reachability of position (cur - 1 - k),
    # where cur is the next position to be processed.
    # Position x = cur is reachable iff some reachable y in [x-B, x-A],
    # i.e. bits (x-1-y) in [A-1, B-1] of mask.
    FULL = (1 << B) - 1
    QUERY = ((1 << (B - A + 1)) - 1) << (A - 1)

    # Square 1 is reachable (L_i > 1 guaranteed, or M = 0).
    # State as if cur = 2: bit 0 = position 1.
    mask = 1
    cur = 2

    def trailing_ones(m):
        s = 0
        while s < B and (m & 1):
            s += 1
            m >>= 1
        return s

    def run_gap(end, need_end):
        """Simulate free cells cur..end.

        If need_end: return reachability of end (bool).
        Else: return True if we can continue past end (window nonzero),
              False if the window zeroed out (nothing further reachable).

        Two fast-forwards keep this O(min(gap_len, 2^B + B)):
        - streak: B consecutive reachable cells imply every later cell in
          the gap is reachable (x-A always lands in the trailing streak).
        - cycle detection: with all cells free, mask evolves
          deterministically; a repeated mask means a period. Skip whole
          periods toward end. (Needed e.g. M=0, A=B: reachable cells are
          isolated with period A, streak never reaches B.)
        """
        nonlocal mask, cur
        streak = trailing_ones(mask)
        seen = {}
        while cur <= end:
            if mask in seen:
                p = cur - seen[mask]
                skip = (end - cur + 1) // p
                if skip > 0:
                    cur += skip * p
                    seen.clear()
                    continue
                # Less than one full period left: fall through and
                # simulate the remaining steps directly.
                seen.clear()
            else:
                seen[mask] = cur
            bit = 1 if (mask & QUERY) else 0
            mask = ((mask << 1) | bit) & FULL
            if cur == end:
                cur += 1
                if need_end:
                    return bool(bit)
                # Past-end continuation only needs a nonzero window.
                return mask != 0
            cur += 1
            if bit:
                streak += 1
                if streak >= B:
                    # All remaining cells in this gap are reachable.
                    mask = FULL
                    cur = end + 1
                    return True
            else:
                streak = 0
            if mask == 0:
                return False
        return True

    ok = True
    for (L, R) in intervals:
        gap_end = L - 1
        if cur <= gap_end:
            if not run_gap(gap_end, False):
                ok = False
                break
        # Bad segment [L, R]: cells are unreachable (shift in zeros).
        seg_len = R - L + 1
        if seg_len >= B:
            # Window becomes all-zero permanently; nothing beyond reachable.
            ok = False
            break
        for _ in range(seg_len):
            mask = (mask << 1) & FULL
            cur += 1
        if mask == 0:
            ok = False
            break

    if ok:
        ok = run_gap(N, True)

    sys.stdout.write("Yes\n" if ok else "No\n")

solve()