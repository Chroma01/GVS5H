import sys

def solve():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    
    items = [[], [], []]  # items[0] for vitamin 1, items[1] for 2, items[2] for 3
    for _ in range(N):
        V = int(data[idx]); idx += 1
        A = int(data[idx]); idx += 1
        C = int(data[idx]); idx += 1
        items[V-1].append((C, A))
    
    # 0/1 knapsack for each vitamin type
    dp = []
    for t in range(3):
        d = [-1] * (X + 1)
        d[0] = 0
        for w, v in items[t]:
            # iterate backwards
            for c in range(X, w - 1, -1):
                if d[c - w] != -1:
                    nv = d[c - w] + v
                    if nv > d[c]:
                        d[c] = nv
        # prefix max: best value using at most c calories
        for c in range(1, X + 1):
            if d[c] < d[c-1]:
                d[c] = d[c-1]
        dp.append(d)
    
    # combine: iterate c1, c2, c3 = X - c1 - c2
    best = 0
    dp1, dp2, dp3 = dp[0], dp[1], dp[2]
    for c1 in range(X + 1):
        v1 = dp1[c1]
        for c2 in range(X - c1 + 1):
            c3 = X - c1 - c2
            v2 = dp2[c2]
            v3 = dp3[c3]
            m = v1
            if v2 < m: m = v2
            if v3 < m: m = v3
            if m > best:
                best = m
    print(best)

solve()