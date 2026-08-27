import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    items = [[] for _ in range(4)]
    for _ in range(N):
        V = int(next(it))
        A = int(next(it))
        C = int(next(it))
        items[V].append((A, C))

    # max_vit[t][c] = maximum vitamin of type t achievable with at most c calories
    max_vit = [None] * 4
    for t in range(1, 4):
        dp = [0] * (X + 1)
        item_list = items[t]
        for a, c in item_list:
            # 0/1 knapsack: iterate calorie budget descending
            for b in range(X, c - 1, -1):
                val = dp[b - c] + a
                if val > dp[b]:
                    dp[b] = val
        # prefix max to convert "exact" to "at most"
        for c in range(1, X + 1):
            if dp[c] < dp[c - 1]:
                dp[c] = dp[c - 1]
        max_vit[t] = dp

    # Binary search on the answer
    lo = 0
    hi = min(max_vit[t][X] for t in range(1, 4))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        total = 0
        feasible = True
        for t in range(1, 4):
            arr = max_vit[t]
            # find minimum calories needed to reach at least mid
            need = X + 1
            for c in range(X + 1):
                if arr[c] >= mid:
                    need = c
                    break
            total += need
            if total > X:
                feasible = False
                break
        if feasible:
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()