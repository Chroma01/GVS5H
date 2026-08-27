import sys
from bisect import bisect_left, bisect_right


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    A = data[1:1 + n]
    B = data[1 + n:1 + 2 * n]
    C = data[1 + 2 * n:1 + 3 * n]

    off = []
    on = []
    common_one = []

    initial_sum = 0
    for a, b, c in zip(A, B, C):
        if a:
            initial_sum += c

        if a == 1 and b == 0:
            off.append(c)
        elif a == 0 and b == 1:
            on.append(c)
        elif a == 1 and b == 1:
            common_one.append(c)

    off.sort()
    on.sort()
    common_one.sort()

    off_sum = sum(off)

    off_prefix = [0]
    for x in off:
        off_prefix.append(off_prefix[-1] + x)

    on_prefix = [0]
    for x in on:
        on_prefix.append(on_prefix[-1] + x)

    # Off-flips are performed in descending C order.
    # With off sorted increasingly, x at index i has coefficient i + 1.
    q_off = sum(x * (i + 1) for i, x in enumerate(off))

    # On-flips are performed in ascending C order.
    # With on sorted increasingly, x at index i has coefficient k - i.
    k = len(on)
    q_on = sum(x * (k - i) for i, x in enumerate(on))

    m = len(off)
    answer = (
        m * initial_sum - q_off
        + k * (initial_sum - off_sum)
        + q_on
    )

    # Add temporary flips for common-one positions in descending order.
    # After r iterations, the selected positions are the r largest costs.
    selected_sum = 0
    total_selected = 0

    for r in range(1, len(common_one) + 1):
        x = common_one[-r]

        # Updating q_off:
        # Existing elements >= x shift one position right.
        p = bisect_left(off, x)
        sum_off_ge = off_prefix[m] - off_prefix[p]
        count_off_lt = p

        q_off += (
            sum_off_ge
            + selected_sum
            + x * (count_off_lt + 1)
        )

        # Updating q_on:
        # Existing elements <= x gain one later operation.
        p = bisect_right(on, x)
        sum_on_le = on_prefix[p]
        count_on_ge = k - bisect_left(on, x)

        q_on += (
            sum_on_le
            + x * (count_on_ge + (r - 1) + 1)
        )

        selected_sum += x
        total_selected += 1

        off_count = m + total_selected
        on_count = k + total_selected
        remaining_sum = initial_sum - off_sum - selected_sum

        total = (
            off_count * initial_sum - q_off
            + on_count * remaining_sum + q_on
        )
        if total < answer:
            answer = total

    print(answer)


if __name__ == "__main__":
    main()