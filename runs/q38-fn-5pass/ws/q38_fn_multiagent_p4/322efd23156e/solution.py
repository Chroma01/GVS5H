import sys
from bisect import bisect_left


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x = data[0], data[1]
    groups = [[], [], []]

    idx = 2
    for _ in range(n):
        v = data[idx]
        a = data[idx + 1]
        c = data[idx + 2]
        idx += 3
        groups[v - 1].append((c, a))

    # If any vitamin cannot be obtained at all, the minimum is always 0.
    if not groups[0] or not groups[1] or not groups[2]:
        print(0)
        return

    dps = []

    for items in groups:
        dp = [0] * (x + 1)

        # 0/1 knapsack: dp[c] = maximum vitamin amount with at most c calories.
        for c, a in items:
            for cap in range(x, c - 1, -1):
                nv = dp[cap - c] + a
                if nv > dp[cap]:
                    dp[cap] = nv

        # Ensure dp is nondecreasing, so dp[c] means "at most c calories".
        for cap in range(1, x + 1):
            if dp[cap] < dp[cap - 1]:
                dp[cap] = dp[cap - 1]

        dps.append(dp)

    # The answer cannot exceed the maximum achievable amount of any vitamin.
    upper = min(dps[0][x], dps[1][x], dps[2][x])

    lo = 0
    hi = upper + 1
    bl = bisect_left

    def feasible(target: int) -> bool:
        total_cost = 0

        for dp in dps:
            # First calorie budget where this vitamin reaches target.
            cost = bl(dp, target)
            if cost > x:
                return False

            total_cost += cost
            if total_cost > x:
                return False

        return True

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    solve()