import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); X = int(data[1])
    groups = [[], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        groups[v - 1].append((a, c))

    totals = [sum(a for a, _ in g) for g in groups]
    if min(totals) == 0:
        print(0)
        return

    cap_val = min(totals)  # answer never exceeds this; cap DP values here
    NEG = -1

    prefs = []
    for g in groups:
        dp = [NEG] * (X + 1)
        dp[0] = 0
        reach = 0  # max calorie index that can be nonzero so far
        for a, c in g:
            hi_j = reach + c
            if hi_j > X:
                hi_j = X
            for j in range(hi_j, c - 1, -1):
                prev = dp[j - c]
                if prev >= 0:
                    val = prev + a
                    if val > cap_val:
                        val = cap_val
                    if val > dp[j]:
                        dp[j] = val
            reach = hi_j
        # convert "exactly c" to "at most c" via prefix maxima (nondecreasing)
        best = dp[0]
        for j in range(1, X + 1):
            if dp[j] < best:
                dp[j] = best
            else:
                best = dp[j]
        prefs.append(dp)

    def feasible(T):
        s = 0
        for p in prefs:
            i = bisect_left(p, T)
            if i > X:
                return False
            s += i
            if s > X:
                return False
        return True

    lo, hi = 0, cap_val
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

main()