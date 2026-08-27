import sys
from bisect import bisect_left, bisect_right


def weighted_order_sum_desc(values):
    values.sort(reverse=True)
    n = len(values)
    return sum((n - i) * x for i, x in enumerate(values))


def weighted_order_sum_asc(values):
    values.sort()
    n = len(values)
    return sum((n - i) * x for i, x in enumerate(values))


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:1 + n]
    b = data[1 + n:1 + 2 * n]
    c = data[1 + 2 * n:1 + 3 * n]

    remove = []   # 1 -> 0
    add = []      # 0 -> 1
    common_one = []  # 1 -> 1

    for ai, bi, ci in zip(a, b, c):
        if ai == 1:
            if bi == 0:
                remove.append(ci)
            else:
                common_one.append(ci)
        elif bi == 1:
            add.append(ci)

    # Values and prefix sums for queries used while considering
    # temporarily turning off the largest common-one weights.
    remove.sort()
    add.sort()
    common_one.sort(reverse=True)

    pref_remove = [0]
    for x in remove:
        pref_remove.append(pref_remove[-1] + x)

    pref_add = [0]
    for x in add:
        pref_add.append(pref_add[-1] + x)

    sum_remove = pref_remove[-1]
    sum_common = sum(common_one)
    initial_sum = sum_remove + sum_common

    # Weighted sums in the required orders:
    # removals in descending order, additions in ascending order.
    wr = weighted_order_sum_desc(remove[:])
    wp = weighted_order_sum_asc(add[:])

    d = len(remove)
    e = len(add)

    # No temporarily disabled common-one bits.
    answer = d * initial_sum - wr + e * sum_common + wp

    selected_sum = 0
    t = 0

    # For a fixed number t, choosing the t largest common-one weights is optimal.
    # Insert them one at a time, from largest to smallest.
    for x in common_one:
        # In descending removal order, use D before T on equal weights.
        # Existing selected common values are all >= x.
        pos_lt_d = bisect_left(remove, x)
        pos_ge_d = pos_lt_d
        sum_ge_d = sum_remove - pref_remove[pos_ge_d]
        cnt_lt_d = pos_lt_d

        # New contribution to descending weighted sum.
        wr += sum_ge_d + selected_sum + x * (cnt_lt_d + 1)

        # In ascending addition order, use E before T on equal weights.
        pos_le_e = bisect_right(add, x)
        sum_le_e = pref_add[pos_le_e]
        cnt_gt_e = e - pos_le_e

        # New contribution to ascending weighted sum.
        wp += sum_le_e + x * (t + cnt_gt_e + 1)

        selected_sum += x
        t += 1

        m = d + t
        k = e + t

        current = (
            m * initial_sum
            - wr
            + k * (sum_common - selected_sum)
            + wp
        )
        if current < answer:
            answer = current

    print(answer)


if __name__ == "__main__":
    main()