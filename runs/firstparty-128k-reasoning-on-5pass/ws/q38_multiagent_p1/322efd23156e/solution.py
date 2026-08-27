import sys
from bisect import bisect_left


def main():
    raw = sys.stdin.buffer.read().split()
    if not raw:
        return

    it = iter(map(int, raw))
    N = next(it)
    X = next(it)

    items = [[] for _ in range(3)]
    for _ in range(N):
        v = next(it)
        a = next(it)
        c = next(it)
        items[v - 1].append((a, c))

    # If any vitamin type has no food, the minimum among the three is always 0.
    if not items[0] or not items[1] or not items[2]:
        print(0)
        return

    dps = []
    x = X

    # For each vitamin type, compute d[c] = max units of this vitamin
    # obtainable with at most c calories.
    for arr in items:
        d = [0] * (x + 1)

        # 0/1 knapsack over calorie capacity.
        # Descending order prevents using the same food multiple times.
        for a, c in arr:
            for cap in range(x, c - 1, -1):
                nv = d[cap - c] + a
                if nv > d[cap]:
                    d[cap] = nv

        # Ensure d is nondecreasing: "at most c" capacity.
        for i in range(1, x + 1):
            if d[i] < d[i - 1]:
                d[i] = d[i - 1]

        dps.append(d)

    d0, d1, d2 = dps

    # Binary search the maximum feasible minimum vitamin intake.
    lo = 0
    hi = min(d0[x], d1[x], d2[x]) + 1
    bl = bisect_left

    while lo + 1 < hi:
        mid = (lo + hi) // 2
        need = bl(d0, mid) + bl(d1, mid) + bl(d2, mid)
        if need <= x:
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    main()