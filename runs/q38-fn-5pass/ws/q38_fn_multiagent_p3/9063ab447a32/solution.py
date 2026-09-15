import sys
import math


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    m = data[1]
    p = data[2:2 + n]
    p.sort()

    p_min = p[0]

    # Upper bound: buy enough units of the cheapest product to exceed M.
    # If a^2 * p_min > M, then the marginal cost (2a - 1) * p_min is safe.
    a = math.isqrt(m // p_min) + 1
    high = (2 * a - 1) * p_min
    low = 0

    def cost_gt(x: int, ps=p, m=m) -> bool:
        """Return True iff total cost of all marginal costs <= x exceeds m."""
        acc = 0
        for pi in ps:
            if pi > x:
                break
            k = (x // pi + 1) >> 1
            acc += k * k * pi
            if acc > m:
                return True
        return False

    # Smallest marginal cost y such that buying all units with cost <= y is too expensive.
    while high - low > 1:
        mid = (low + high) >> 1
        if cost_gt(mid):
            high = mid
        else:
            low = mid

    y = high

    # Count and cost of all units with marginal cost < y.
    # Also count how many units have marginal cost exactly y.
    less_count = 0
    less_cost = 0
    equal_count = 0

    for pi in p:
        if pi > y:
            break

        q = y // pi
        k_y = (q + 1) >> 1

        # y is a marginal cost of this product iff y = (odd) * pi.
        if (q & 1) and q * pi == y:
            k_less = k_y - 1
            equal_count += 1
        else:
            k_less = k_y

        less_count += k_less
        less_cost += k_less * k_less * pi

    rem = m - less_cost
    add = rem // y
    if add > equal_count:
        add = equal_count

    print(less_count + add)


if __name__ == "__main__":
    main()