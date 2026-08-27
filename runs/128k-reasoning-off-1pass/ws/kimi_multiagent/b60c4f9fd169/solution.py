import sys

def solve():
    data = sys.stdin.buffer.read().split()
    K = int(data[0])
    S = data[1]          # bytes: indexing gives ints, ideal for hashing
    T = data[2]
    N = len(S)
    M = len(T)
    out = sys.stdout.write

    # Necessary condition: length difference must be bridgeable
    if abs(N - M) > K:
        out("No\n")
        return

    # ---- Rolling hash (mod 2^64) for O(log)-time LCP queries ----
    MASK = (1 << 64) - 1
    B = 91138233
    L = N if N > M else M
    powB = [1] * (L + 1)
    for i in range(1, L + 1):
        powB[i] = (powB[i - 1] * B) & MASK

    HS = [0] * (N + 1)
    h = 0
    for i in range(N):
        h = ((h * B) + S[i]) & MASK
        HS[i + 1] = h
    HT = [0] * (M + 1)
    h = 0
    for i in range(M):
        h = ((h * B) + T[i]) & MASK
        HT[i + 1] = h

    def lcp(i, j):
        # length of longest common prefix of S[i:] and T[j:]
        lo = 0
        hi = N - i
        if M - j < hi:
            hi = M - j
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            h1 = (HS[i + mid] - ((HS[i] * powB[mid]) & MASK)) & MASK
            h2 = (HT[j + mid] - ((HT[j] * powB[mid]) & MASK)) & MASK
            if h1 == h2:
                lo = mid
            else:
                hi = mid - 1
        return lo

    # ---- Myers furthest-reaching diagonal DP ----
    # f[e][d] = max i such that S[:i] -> T[:i+d] with at most e edits (d = j - i)
    NEG = -1
    OFF = K + 1
    W = 2 * K + 3
    prev = [NEG] * W
    prev[OFF] = lcp(0, 0)          # e = 0: only diagonal 0
    target = M - N

    if prev[target + OFF] == N:    # reachable with 0 edits (S == T)
        out("Yes\n")
        return

    for e in range(1, K + 1):
        cur = [NEG] * W
        for d in range(-e, e + 1):
            best = NEG
            # insertion: arrive at d from d-1, i unchanged (need previous j < M)
            v = prev[d - 1 + OFF]
            if v >= 0 and v + d - 1 < M and v > best:
                best = v
            # deletion: arrive at d from d+1, consume one S char (need i < N)
            v = prev[d + 1 + OFF]
            if v >= 0 and v < N and v + 1 > best:
                best = v + 1
            # substitution: stay on d, consume both (need i < N and j < M)
            v = prev[d + OFF]
            if v >= 0 and v < N and v + d < M and v + 1 > best:
                best = v + 1
            if best < 0:
                continue
            # extend along free matches
            best += lcp(best, best + d)
            cur[d + OFF] = best
        if cur[target + OFF] >= N:       # reached (N, M)
            out("Yes\n")
            return
        prev = cur

    out("No\n")

solve()