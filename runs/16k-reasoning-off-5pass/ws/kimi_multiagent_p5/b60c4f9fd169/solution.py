import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split(b"\n")
    K = int(data[0].strip())
    S = data[1].rstrip(b"\r")
    T = data[2].rstrip(b"\r")

    n, m = len(S), len(T)

    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return

    # LCP length of S[i:] and T[j:] via binary search on bytes slices (C-speed).
    def lcp(i: int, j: int) -> int:
        maxlen = min(n - i, m - j)
        lo, hi = 0, maxlen
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            if S[i:i + mid] == T[j:j + mid]:
                lo = mid
            else:
                hi = mid - 1
        return lo

    NEG = -10 ** 9
    # reach[d + K] = furthest i (index in S) reachable on diagonal d = i - j
    # with at most (current e) edits.
    reach = [NEG] * (2 * K + 3)

    # 0 edits: only diagonal 0, extend through matches.
    reach[K] = lcp(0, 0)
    if reach[K] >= n and n - m == 0:
        sys.stdout.write("Yes\n")
        return

    for e in range(1, K + 1):
        prev = reach
        reach = [NEG] * (2 * K + 3)
        for d in range(-e, e + 1):
            best = NEG
            # insertion (advance j, i unchanged): from diagonal d+1
            v = prev[d + 1 + K]
            if v > best:
                best = v
            # deletion (advance i by 1): from diagonal d-1
            v = prev[d - 1 + K] + 1
            if v > best:
                best = v
            # substitution (advance both): same diagonal
            v = prev[d + K] + 1
            if v > best:
                best = v
            if best < 0:
                continue
            if best > n:
                best = n
            # j = i - d must stay within [0, m]
            j = best - d
            if j < 0:
                continue
            if j > m:
                best = m + d
                j = m
            if best >= n and j >= m:
                reach[d + K] = best
                continue
            reach[d + K] = best + lcp(best, j)
        dnm = n - m
        if -e <= dnm <= e and reach[dnm + K] >= n:
            sys.stdout.write("Yes\n")
            return

    sys.stdout.write("No\n")


solve()