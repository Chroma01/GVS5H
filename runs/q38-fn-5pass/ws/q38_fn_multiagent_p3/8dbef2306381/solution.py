import sys
from heapq import heappush, heappop


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, A, B = data[0], data[1], data[2], data[3]

    intervals = []
    p = 4
    for _ in range(M):
        l = data[p]
        r = data[p + 1]
        p += 2
        intervals.append((l, r))

    # Merge bad intervals, including adjacent ones.
    if intervals:
        intervals.sort()
        merged = []
        for l, r in intervals:
            if merged and l <= merged[-1][1] + 1:
                if r > merged[-1][1]:
                    merged[-1] = (merged[-1][0], r)
            else:
                merged.append((l, r))
        intervals = merged

        # Safety checks for invalid inputs; constraints guarantee these do not happen.
        if intervals[0][0] <= 1 or intervals[-1][1] >= N:
            print("No")
            return

        # A bad block of length >= B cannot be crossed.
        for l, r in intervals:
            if r - l + 1 >= B:
                print("No")
                return

    # Build maximal safe segments.
    starts = []
    ends = []
    cur = 1
    for l, r in intervals:
        if cur <= l - 1:
            starts.append(cur)
            ends.append(l - 1)
        cur = r + 1
    if cur <= N:
        starts.append(cur)
        ends.append(N)

    S = len(starts)

    # min_dist[r] = minimum representable distance congruent to r modulo A
    # using jumps in [A, B].  Step A is a self-loop modulo A, so it is enough
    # to relax with A+1..B.
    INF = 10**30
    min_dist = [INF] * A
    min_dist[0] = 0
    heap = [(0, 0)]

    while heap:
        d, r = heappop(heap)
        if d != min_dist[r]:
            continue
        for step in range(A + 1, B + 1):
            nr = (r + step) % A
            nd = d + step
            if nd < min_dist[nr]:
                min_dist[nr] = nd
                heappush(heap, (nd, nr))

    # trans_masks[L][delta]:
    # For a segment whose last window has length L, this is the bitmask of
    # exit offsets that can jump to y = end + delta with a jump length in [A, B].
    trans_masks = [[0] * (B + 1) for _ in range(B + 1)]
    for L in range(1, B + 1):
        for delta in range(1, B + 1):
            low = delta + L - 1 - B
            if low < 0:
                low = 0
            high = delta + L - 1 - A
            if high >= L:
                high = L - 1
            if low <= high:
                trans_masks[L][delta] = ((1 << (high - low + 1)) - 1) << low

    reach = [0] * S
    if S:
        reach[0] = 1

    md = min_dist
    a = A
    st = starts
    en = ends
    S_local = S
    N_local = N

    for k in range(S_local):
        mask = reach[k]
        if not mask:
            continue

        s = st[k]
        e = en[k]
        length = e - s + 1

        first_len = B if length >= B else length
        mask &= (1 << first_len) - 1
        if not mask:
            continue

        last_start = e - B + 1
        if last_start < s:
            last_start = s
        L = e - last_start + 1
        base = last_start - s

        # can_bits has bit (delta + B) set iff base + delta is representable.
        can_bits = 0
        min_delta = 1 - first_len
        max_delta = L - 1
        for delta in range(min_delta, max_delta + 1):
            d = base + delta
            if d >= 0 and d >= md[d % a]:
                can_bits |= 1 << (delta + B)

        mask_last = (1 << L) - 1
        exits = 0

        m = mask
        while m:
            lsb = m & -m
            ei = lsb.bit_length() - 1
            exits |= (can_bits >> (B - ei)) & mask_last
            m ^= lsb

        if not exits:
            continue

        # Last segment: N is its last position.
        if k == S_local - 1:
            if exits & (1 << (L - 1)):
                print("Yes")
                return
            continue

        # Try all landings y = e + delta, 1 <= delta <= B.
        j = k + 1
        masks_L = trans_masks[L]

        for delta in range(1, B + 1):
            y = e + delta
            if y > N_local:
                break

            while j < S_local and en[j] < y:
                j += 1

            if j >= S_local:
                break

            if st[j] <= y:
                msk = masks_L[delta]
                if msk and (exits & msk):
                    off = y - st[j]
                    reach[j] |= 1 << off

    print("No")


if __name__ == "__main__":
    solve()