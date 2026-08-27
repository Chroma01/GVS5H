import sys

def solve() -> None:
    input = sys.stdin.readline
    first = input().split()
    if not first:
        return
    N, X = map(int, first)

    foods = [[] for _ in range(3)]
    total_amount = [0, 0, 0]

    for _ in range(N):
        V, A, C = map(int, input().split())
        foods[V - 1].append((A, C))
        total_amount[V - 1] += A

    # DP for each vitamin: best[v][c] = max amount of vitamin v with at most c calories
    best = []
    for v in range(3):
        dp = [-1] * (X + 1)
        dp[0] = 0
        for a, c in foods[v]:
            # iterate backwards for 0/1 knapsack
            for w in range(X, c - 1, -1):
                if dp[w - c] != -1:
                    val = dp[w - c] + a
                    if val > dp[w]:
                        dp[w] = val
        # make it prefix maximum (max amount with <= w calories)
        for w in range(1, X + 1):
            if dp[w] < dp[w - 1]:
                dp[w] = dp[w - 1]
        best.append(dp)

    def feasible(t: int) -> bool:
        used = 0
        for v in range(3):
            # find smallest calories w such that best[v][w] >= t
            w = 0
            while w <= X and best[v][w] < t:
                w += 1
            if w > X:  # impossible for this vitamin
                return False
            used += w
            if used > X:
                return False
        return used <= X

    lo = 0
    hi = min(total_amount)  # obvious upper bound

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(lo)


if __name__ == "__main__":
    solve()