import sys
from bisect import bisect_left, bisect_right


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:1 + n]
    b = data[1 + n:1 + 2 * n]
    c = data[1 + 2 * n:1 + 3 * n]

    initial_sum = sum(x * y for x, y in zip(a, c))

    neg = []       # Mandatory 1 -> 0 magnitudes, descending
    pos = []       # Mandatory 0 -> 1 magnitudes, ascending
    optional = []  # A_i = B_i = 1, descending

    for ai, bi, ci in zip(a, b, c):
        if ai == 1 and bi == 0:
            neg.append(ci)
        elif ai == 0 and bi == 1:
            pos.append(ci)
        elif ai == 1 and bi == 1:
            optional.append(ci)

    neg.sort(reverse=True)
    pos.sort()
    optional.sort(reverse=True)

    q = len(neg)
    r = len(pos)

    neg_sum = sum(neg)
    pos_sum = sum(pos)

    weighted_neg = sum((q - i) * x for i, x in enumerate(neg))
    weighted_pos = sum((r - i) * x for i, x in enumerate(pos))

    answer = (
        (q + r) * initial_sum
        - weighted_neg
        - r * neg_sum
        + weighted_pos
    )

    # Prefix sums for range-sum queries on mandatory events.
    neg_asc = neg[::-1]
    neg_prefix = [0]
    for x in neg_asc:
        neg_prefix.append(neg_prefix[-1] + x)

    pos_prefix = [0]
    for x in pos:
        pos_prefix.append(pos_prefix[-1] + x)

    # optional is descending. Negative optional values are ascending.
    neg_optional = [-x for x in optional]
    optional_prefix = [0]
    for x in optional:
        optional_prefix.append(optional_prefix[-1] + x)

    selected_sum = 0

    for k, x in enumerate(optional, 1):
        previous_selected = k - 1

        # In the descending negative list, only existing values greater
        # than x increase their coefficient when x is inserted.
        first_equal = bisect_left(neg_optional, -x)
        mandatory_greater_count = len(neg) - bisect_right(neg_asc, x)
        mandatory_greater_sum = (
            neg_prefix[len(neg)] - neg_prefix[bisect_right(neg_asc, x)]
        )
        selected_greater_sum = optional_prefix[first_equal]

        negative_le_count = (
            bisect_right(neg_asc, x)
            + (previous_selected - first_equal)
        )

        weighted_neg += (
            mandatory_greater_sum
            + selected_greater_sum
            + (negative_le_count + 1) * x
        )

        # In the ascending positive list, only existing values less than
        # x increase their coefficient when x is inserted.
        mandatory_less_index = bisect_left(pos, x)
        mandatory_less_sum = pos_prefix[mandatory_less_index]

        positive_ge_count = (
            len(pos) - bisect_left(pos, x)
            + previous_selected
        )

        weighted_pos += (
            mandatory_less_sum
            + (positive_ge_count + 1) * x
        )

        q += 1
        r += 1
        neg_sum += x
        pos_sum += x
        selected_sum += x

        current = (
            (q + r) * initial_sum
            - weighted_neg
            - r * neg_sum
            + weighted_pos
        )
        answer = min(answer, current)

    print(answer)


if __name__ == "__main__":
    solve()