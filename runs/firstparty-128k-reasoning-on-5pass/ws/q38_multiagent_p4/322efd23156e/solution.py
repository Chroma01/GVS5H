import sys
from bisect import bisect_left


def build_dp(items, X):
    groups = {}
    for a, c in items:
        groups.setdefault(c, []).append(a)

    if not groups:
        return [0] * (X + 1)

    groups_list = []
    for c, arr in groups.items():
        k = X // c
        if k <= 0:
            continue
        arr.sort(reverse=True)
        if len(arr) > k:
            arr = arr[:k]
        if arr:
            work = len(arr) * (X - c + 1)
            groups_list.append((c, arr, work))

    if not groups_list:
        return [0] * (X + 1)

    # Seed the cost group with the largest estimated 0/1 update work.
    init_idx = max(
        range(len(groups_list)),
        key=lambda i: (groups_list[i][2], len(groups_list[i][1]), groups_list[i][0]),
    )
    init_c, init_arr, _ = groups_list[init_idx]

    # Directly fill DP for the seed group. All items in it have the same cost,
    # so the best value for capacity j is the prefix sum of the largest items
    # that fit in j.
    dp = [0] * (X + 1)
    p = 0
    idx = 0
    L = len(init_arr)
    next_cost = init_c
    for j in range(X + 1):
        while idx < L and next_cost <= j:
            p += init_arr[idx]
            idx += 1
            next_cost += init_c
        dp[j] = p

    # Process all remaining pruned items with standard descending 0/1 updates.
    d = dp
    xx = X
    for i, (c, arr, _) in enumerate(groups_list):
        if i == init_idx:
            continue
        cc = c
        for a in arr:
            aa = a
            for j in range(xx, cc - 1, -1):
                nv = d[j - cc] + aa
                if nv > d[j]:
                    d[j] = nv

    # Ensure the array is nondecreasing for bisect_left.
    for j in range(1, xx + 1):
        if d[j] < d[j - 1]:
            d[j] = d[j - 1]

    return d


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    X = data[1]
    items = [[], [], []]
    totals = [0, 0, 0]

    idx = 2
    for _ in range(N):
        v = data[idx] - 1
        a = data[idx + 1]
        c = data[idx + 2]
        idx += 3
        items[v].append((a, c))
        totals[v] += a

    if min(totals) == 0:
        print(0)
        return

    dps = [build_dp(items[v], X) for v in range(3)]

    lo = 0
    hi = min(dp[X] for dp in dps) + 1

    def feasible(t):
        total = 0
        for dp in dps:
            pos = bisect_left(dp, t)
            if pos > X:
                return False
            total += pos
            if total > X:
                return False
        return True

    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid + 1
        else:
            hi = mid

    print(lo - 1)


if __name__ == "__main__":
    main()