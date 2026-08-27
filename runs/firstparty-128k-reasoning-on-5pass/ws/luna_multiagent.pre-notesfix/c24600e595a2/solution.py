import sys
from bisect import bisect_right


def main():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))

    initial_weight = sum(ai * ci for ai, ci in zip(a, c))

    down = sorted(
        ci for ai, bi, ci in zip(a, b, c)
        if ai == 1 and bi == 0
    )
    up = sorted(
        ci for ai, bi, ci in zip(a, b, c)
        if ai == 0 and bi == 1
    )
    optional = sorted(
        ci for ai, bi, ci in zip(a, b, c)
        if ai == 1 and bi == 1
    )

    d = len(down)
    u = len(up)
    m = len(optional)

    down_sum = sum(down)
    up_sum = sum(up)

    # Cost of mandatory deactivations, processed in descending C order.
    down_cost = sum((i + 1) * x for i, x in enumerate(down))

    # Cost of mandatory activations, processed in ascending C order.
    up_cost = sum((u - i) * x for i, x in enumerate(up))

    # No optional temporary deactivations.
    base = (
        (d + u) * initial_weight
        - u * down_sum
        - down_cost
        + up_cost
    )

    # Prefix sums for binary-search range sums.
    pref_down = [0] * (d + 1)
    for i, x in enumerate(down):
        pref_down[i + 1] = pref_down[i] + x

    pref_up = [0] * (u + 1)
    for i, x in enumerate(up):
        pref_up[i + 1] = pref_up[i] + x

    # Prefix sums involving original indices in the sorted optional array.
    pref_optional = [0] * (m + 1)
    pref_indexed = [0] * (m + 1)
    for i, x in enumerate(optional):
        pref_optional[i + 1] = pref_optional[i] + x
        pref_indexed[i + 1] = pref_indexed[i] + i * x

    answer = base

    # Choose the suffix optional[t:].
    # For a fixed number of selected optional bits, an optimal choice is
    # always a suffix of the sorted optional costs.
    for t in range(m + 1):
        s = m - t
        selected_sum = pref_optional[m] - pref_optional[t]

        # Sum of the individual terms h(x), excluding pair interactions.
        individual = s * (2 * initial_weight - down_sum)

        for x in optional[t:]:
            down_le_count = bisect_right(down, x)
            down_le_sum = pref_down[down_le_count]
            down_ge_sum = down_sum - down_le_sum

            up_le_count = bisect_right(up, x)
            up_le_sum = pref_up[up_le_count]
            up_ge_count = u - up_le_count

            h = (
                2 * initial_weight
                - down_sum
                - (u + s) * x
                + x * (up_ge_count - down_le_count)
                + up_le_sum
                - down_ge_sum
            )
            individual += h - (2 * initial_weight - down_sum)

        # Pair contribution for selected values z_i <= z_j is -(z_j-z_i).
        selected_indexed_sum = pref_indexed[m] - pref_indexed[t]
        pair_difference = (
            2 * selected_indexed_sum
            - (t + m - 1) * selected_sum
        )

        value = base + individual - pair_difference
        if value < answer:
            answer = value

    print(answer)


if __name__ == "__main__":
    main()