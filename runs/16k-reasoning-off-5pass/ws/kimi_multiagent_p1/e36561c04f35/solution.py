import sys
from collections import defaultdict

def solve_case(a):
    n = len(a)
    dp = [0] * (n + 1)
    occ = defaultdict(list)
    for idx, v in enumerate(a, 1):
        occ[v].append(idx)

    # F(seq): same DP on a filtered subsequence (memoized)
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def F(seq):
        m = len(seq)
        if m <= 1:
            return m
        dp2 = [0] * (m + 1)
        for i in range(1, m + 1):
            v = seq[i - 1]
            best = dp2[i - 1] + 1
            cnt = 0
            cross = 0
            inner = []
            for j in range(i, 0, -1):
                if seq[j - 1] == v:
                    if j < i:
                        cnt += 1
                        cross += len(inner)
                    cand = dp2[j - 1] + F(tuple(inner)) + cross + 1
                    if cand < best:
                        best = cand
                else:
                    inner.insert(0, seq[j - 1])
                    cross += cnt
            dp2[i] = best
        return dp2[m]

    for i in range(1, n + 1):
        v = a[i - 1]
        best = dp[i - 1] + 1
        for j in reversed(occ[v]):
            if j > i:
                continue
            if j == i:
                cand = dp[j - 1] + 1
                if cand < best:
                    best = cand
                continue
            cnt = 0
            cross = 0
            inner = []
            for x in range(j, i + 1):
                if a[x - 1] == v:
                    cnt += 1
                else:
                    cross += cnt
                    inner.append(a[x - 1])
            if dp[j - 1] + cross + 1 >= best:
                if cross + 1 >= best:
                    break
                continue
            cand = dp[j - 1] + F(tuple(inner)) + cross + 1
            if cand < best:
                best = cand
        dp[i] = best
    return dp[n]

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    p = 1
    out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        a = list(map(int, data[p:p + n])); p += n
        out.append(str(solve_case(a)))
    sys.stdout.write("\n".join(out) + "\n")

main()