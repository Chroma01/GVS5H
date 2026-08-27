import sys
from bisect import bisect_left, bisect_right


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:1 + n]
    b = data[1 + n:1 + 2 * n]
    c = data[1 + 2 * n:1 + 3 * n]

    removals = []
    additions = []
    persistent = []

    for ai, bi, ci in zip(a, b, c):
        if ai == 1 and bi == 0:
            removals.append(ci)
        elif ai == 0 and bi == 1:
            additions.append(ci)
        elif ai == 1 and bi == 1:
            persistent.append(ci)

    removals.sort(reverse=True)
    additions.sort()
    persistent.sort(reverse=True)

    d = len(removals)
    q = len(additions)
    h = len(persistent)

    sum_r = sum(removals)
    sum_p = sum(persistent)
    initial_sum = sum_r + sum_p

    removals_asc = sorted(removals)
    rem_prefix = [0]
    for x in removals_asc:
        rem_prefix.append(rem_prefix[-1] + x)

    additions_prefix = [0]
    for x in additions:
        additions_prefix.append(additions_prefix[-1] + x)

    persistent_asc = sorted(persistent)

    removal_f = sum(x * (d - i) for i, x in enumerate(removals))
    activation_g = sum(x * (q - i) for i, x in enumerate(additions))

    best = None
    selected_sum = 0

    for p in range(h + 1):
        unselected_sum = sum_p - selected_sum
        removal_count = d + p
        activation_count = q + p

        removal_cost = removal_count * initial_sum - removal_f
        activation_cost = activation_count * unselected_sum + activation_g
        total = removal_cost + activation_cost

        if best is None or total < best:
            best = total

        if p == h:
            break

        x = persistent[p]

        idx = bisect_left(removals_asc, x)
        sum_r_ge = sum_r - rem_prefix[idx]
        count_r_lt = idx

        removal_f += sum_r_ge + selected_sum + x * count_r_lt

        idx = bisect_right(additions, x)
        sum_add_le = additions_prefix[idx]
        count_add_gt = q - idx

        count_selected_greater = h - bisect_right(persistent_asc, x)
        count_selected_equal = p - count_selected_greater

        activation_g += (
            sum_add_le
            + x * count_selected_equal
            + x * (count_add_gt + count_selected_greater)
        )

        selected_sum += x

    print(best)


if __name__ == "__main__":
    solve()