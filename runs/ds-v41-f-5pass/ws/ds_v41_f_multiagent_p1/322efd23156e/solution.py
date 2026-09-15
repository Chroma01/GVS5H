import sys
from bisect import bisect_left

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, X = data[0], data[1]
    groups = [[] for _ in range(3)]
    idx = 2
    for _ in range(N):
        V = data[idx]
        A = data[idx + 1]
        C = data[idx + 2]
        idx += 3
        groups[V - 1].append((C, A))

    dps = []
    for g in groups:
        g.sort()  # sort by calorie cost ascending
        dp = [-10**18] * (X + 1)
        dp[0] = 0
        maxc = 0
        d = dp
        for c, a in g:
            new_maxc = maxc + c
            if new_maxc > X:
                new_maxc = X
            # 0/1 knapsack over exact cost
            for j in range(new_maxc, c - 1, -1):
                v = d[j - c] + a
                if v > d[j]:
                    d[j] = v
            maxc = new_maxc
        # convert exact-cost DP to at-most-cost DP
        for j in range(1, X + 1):
            if dp[j - 1] > dp[j]:
                dp[j] = dp[j - 1]
        dps.append(dp)

    hi = min(dps[0][X], dps[1][X], dps[2][X])
    lo = 0
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        total_cost = 0
        possible = True
        for dp in dps:
            pos = bisect_left(dp, mid)
            total_cost += pos
            if total_cost > X:
                possible = False
                break
        if possible:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    main()