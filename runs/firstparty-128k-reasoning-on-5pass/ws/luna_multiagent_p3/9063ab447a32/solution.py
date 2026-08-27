import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, m = data[0], data[1]
    prices = data[2:]
    min_price = min(prices)

    def total_cost(x):
        total = 0
        for p in prices:
            q = (x // p + 1) // 2
            total += p * q * q
            if total > m:
                return total
        return total

    lo = 0
    hi = 2 * m * min_price + 1

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if total_cost(mid) <= m:
            lo = mid
        else:
            hi = mid

    units_below = 0
    cost_below = 0

    for p in prices:
        q = (lo // p + 1) // 2
        units_below += q
        cost_below += p * q * q

    boundary_units = 0
    for p in prices:
        if hi % p == 0 and ((hi // p) & 1):
            boundary_units += 1

    answer = units_below + min(boundary_units, (m - cost_below) // hi)
    print(answer)


if __name__ == "__main__":
    solve()