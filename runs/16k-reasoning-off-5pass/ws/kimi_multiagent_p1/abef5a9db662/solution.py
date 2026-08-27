import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; p += 1
    contests = []
    for _ in range(N):
        L = data[p]; R = data[p+1]; p += 2
        contests.append((L, R))
    Q = data[p]; p += 1
    queries = data[p:p+Q]

    # Coordinate-compress to distinct query values (each start evolves independently,
    # and we only need answers at query points).
    xs = sorted(set(queries))
    K = len(xs)

    # State representation:
    #   cur[i] = current rating for start xs[i]; monotone non-decreasing in i.
    #   d[i] = cur[i] - xs[i]; diff[i] = d[i] - d[i+1] for i in [0, K-2]; base = d[K-1].
    #   t[i] = xs[i] - ps[i-1] (ps = prefix sum of diff); t is monotone non-decreasing
    #          because t[i+1] - t[i] = cur[i+1] - cur[i] >= 0.
    #   cur[i] = t[i] + base + total, where total = sum of all diff.
    # A contest [L, R] adds 1 to d on the contiguous index range [a, b]
    # (a = first with cur >= L, b = last with cur <= R), which is exactly:
    #   diff[a-1] -= 1 (if a >= 1), diff[b] += 1 (if b <= K-2), else base += 1.
    #
    # Segment tree over diff: node stores
    #   s  = sum of diff in range
    #   mn = min over positions i in range of (xs[i] - ps_within_before(i))
    #   mx = max likewise
    # Combine: mn = min(mnL, mnR - sL), mx = max(mxL, mxR - sL), s = sL + sR.
    S = 1
    while S < K:
        S <<= 1
    NEG = -10**18
    POS = 10**18
    sm = [0] * (2 * S)
    mn = [0] * (2 * S)
    mx = [0] * (2 * S)
    for i in range(K):
        mn[S + i] = xs[i]
        mx[S + i] = xs[i]
    for i in range(K, S):
        mn[S + i] = POS   # padding: never a valid "<= T" candidate
        mx[S + i] = NEG   # padding: never a valid ">= T" candidate
    for v in range(S - 1, 0, -1):
        l = v << 1; r = l | 1
        sl = sm[l]
        sm[v] = sl + sm[r]
        a = mn[l]; b = mn[r] - sl
        mn[v] = a if a < b else b
        a = mx[l]; b = mx[r] - sl
        mx[v] = a if a > b else b

    base = 0
    total = 0  # sum of all diff (may be negative)

    def point_update(pos, delta):
        # diff[pos] += delta ; pos in [0, K-2]
        nonlocal total
        total += delta
        v = S + pos
        sm[v] += delta
        mn[v] -= delta
        mx[v] -= delta
        v >>= 1
        while v:
            l = v << 1; r = l | 1
            sl = sm[l]
            sm[v] = sl + sm[r]
            a = mn[l]; b = mn[r] - sl
            mn[v] = a if a < b else b
            a = mx[l]; b = mx[r] - sl
            mx[v] = a if a > b else b
            v >>= 1

    def find_first_ge(T):
        # first leaf index i with t[i] >= T, or K if none
        if mx[1] < T:
            return K
        v = 1
        acc = 0  # sum of diff over skipped left parts
        while v < S:
            l = v << 1; r = l | 1
            if mx[l] - acc >= T:
                v = l
            else:
                acc += sm[l]
                v = r
        return v - S

    def find_last_le(T):
        # last leaf index i with t[i] <= T, or -1 if none
        if mn[1] > T:
            return -1
        v = 1
        acc = 0
        while v < S:
            l = v << 1; r = l | 1
            if mn[r] - acc <= T:
                v = r
            else:
                v = l
        return v - S

    for (L, R) in contests:
        off = base + total
        a = find_first_ge(L - off)
        if a >= K:
            continue
        b = find_last_le(R - off)
        if b < a:
            continue
        if a >= 1:
            point_update(a - 1, -1)
        if b <= K - 2:
            point_update(b, +1)
        else:
            base += 1

    # Final answers: cur[i] = xs[i] - ps[i-1] + base + total.
    off = base + total
    res = {}
    ps = 0
    for i in range(K):
        res[xs[i]] = xs[i] - ps + off
        if i <= K - 2:
            ps += sm[S + i]
    out = []
    for x in queries:
        out.append(str(res[x]))
    sys.stdout.write("\n".join(out) + "\n")

main()