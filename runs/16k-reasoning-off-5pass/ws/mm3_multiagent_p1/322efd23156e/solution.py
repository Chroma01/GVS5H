import sys

def solve():
    input = sys.stdin.readline
    N, X = map(int, input().split())
    items = [[], [], []]
    total = [0, 0, 0]
    for _ in range(N):
        V, A, C = map(int, input().split())
        items[V-1].append((A, C))
        total[V-1] += A

    # DP for each vitamin type: dp[w] = max vitamin with calories <= w
    dps = []
    for k in range(3):
        dp = [0] * (X + 1)
        for A, C in items[k]:
            for w in range(X, C - 1, -1):
                val = dp[w - C] + A
                if val > dp[w]:
                    dp[w] = val
        dps.append(dp)

    def can(M):
        cost = 0
        for k in range(3):
            dp = dps[k]
            for w in range(X + 1):
                if dp[w] >= M:
                    cost += w
                    break
            else:
                return False
        return cost <= X

    lo = 0
    hi = min(total)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()