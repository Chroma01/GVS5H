import sys

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    foods = [[], [], []]  # index 0,1,2 for vitamin 1,2,3
    for _ in range(N):
        v = int(next(it)) - 1
        a = int(next(it))
        c = int(next(it))
        foods[v].append((a, c))
    
    # knapsack per vitamin: best[c] = max vitamin amount with cost exactly c (or <=c after prefix max)
    best = [None, None, None]
    for t in range(3):
        dp = [-1] * (X + 1)
        dp[0] = 0
        for a, c in foods[t]:
            # 0/1 knapsack, iterate c descending
            for w in range(X - c, -1, -1):
                if dp[w] != -1:
                    nv = dp[w] + a
                    if nv > dp[w + c]:
                        dp[w + c] = nv
        # convert to best[c] = max amount with cost <= c
        cur = 0
        best_arr = [0] * (X + 1)
        for c in range(X + 1):
            if dp[c] > cur:
                cur = dp[c]
            best_arr[c] = cur
        best[t] = best_arr
    
    # upper bound for binary search: max vitamin amount achievable for any type within X calories
    ub = max(best[t][X] for t in range(3))
    
    # feasibility check: can we get at least target units of each vitamin within X calories?
    def feasible(target):
        total_cost = 0
        for t in range(3):
            arr = best[t]
            # find minimal c such that arr[c] >= target
            # arr is non-decreasing
            lo, hi = 0, X
            # binary search for first index with value >= target
            # if not found, return infeasible
            found = -1
            while lo <= hi:
                mid = (lo + hi) // 2
                if arr[mid] >= target:
                    found = mid
                    hi = mid - 1
                else:
                    lo = mid + 1
            if found == -1:
                return False
            total_cost += found
            if total_cost > X:
                return False
        return total_cost <= X
    
    # binary search on answer
    lo, hi = 0, ub
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    print(ans)

if __name__ == "__main__":
    solve()