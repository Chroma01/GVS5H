import sys
from bisect import bisect_left, bisect_right


def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))

    initial_sum = sum(ai * ci for ai, ci in zip(a, c))

    off_required = []
    on_required = []
    temporary = []

    for ai, bi, ci in zip(a, b, c):
        if ai == 1 and bi == 0:
            off_required.append(ci)
        elif ai == 0 and bi == 1:
            on_required.append(ci)
        elif ai == 1 and bi == 1:
            temporary.append(ci)

    off_required.sort(reverse=True)
    on_required.sort()
    temporary.sort(reverse=True)

    p = len(off_required)
    q = len(on_required)

    off_asc = off_required[::-1]
    on_asc = on_required

    off_prefix = [0]
    for value in off_asc:
        off_prefix.append(off_prefix[-1] + value)

    on_prefix = [0]
    for value in on_asc:
        on_prefix.append(on_prefix[-1] + value)

    # q-value for the required off-flips, in descending cost order.
    off_q = 0
    off_sum = 0
    for value in off_required:
        off_q += off_sum + value
        off_sum += value

    # q-value for the required on-flips, in ascending cost order.
    on_q = 0
    on_sum = 0
    for value in on_required:
        on_q += on_sum + value
        on_sum += value

    best = (
        p * initial_sum - off_q
        + q * (initial_sum - off_sum)
        + on_q
    )

    temporary_sum = 0

    for r, value in enumerate(temporary, 1):
        # Insert this temporary off-flip into descending order.
        # Existing required values >= value are before it.
        off_before_count = p - bisect_left(off_asc, value)
        off_before_sum = off_prefix[p] - off_prefix[bisect_left(off_asc, value)]
        off_before_sum += temporary_sum

        off_after_count = bisect_left(off_asc, value)

        off_q += off_before_sum + value * (off_after_count + 1)
        off_sum += value

        # Insert this temporary on-flip into ascending order.
        # Prior temporary bits are larger and therefore after it.
        on_pos = bisect_left(on_asc, value)
        on_before_sum = on_prefix[on_pos]

        on_after_count = q - on_pos + (r - 1)

        on_q += on_before_sum + value * (on_after_count + 1)
        on_sum += value
        temporary_sum += value

        k = p + r
        l = q + r
        base = initial_sum - off_sum

        current = k * initial_sum - off_q + l * base + on_q
        best = min(best, current)

    print(best)


if __name__ == "__main__":
    solve()