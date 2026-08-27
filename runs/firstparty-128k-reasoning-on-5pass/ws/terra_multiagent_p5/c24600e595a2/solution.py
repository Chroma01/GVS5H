import sys
from bisect import bisect_left, bisect_right

def main():
    input = sys.stdin.buffer.readline

    n = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    C = list(map(int, input().split()))

    remove = []
    add = []
    common = []

    initial_sum = 0
    final_sum = 0

    for a, b, c in zip(A, B, C):
        if a:
            initial_sum += c
        if b:
            final_sum += c

        if a == 1 and b == 0:
            remove.append(c)
        elif a == 0 and b == 1:
            add.append(c)
        elif a == 1 and b == 1:
            common.append(c)

    # Required removals are done in decreasing weight order.
    remove.sort(reverse=True)
    d = len(remove)

    # Required additions are done in increasing weight order.
    add.sort()
    u = len(add)
    add_sum = sum(add)

    # Prefix sums of fixed removals in increasing order.
    remove_asc = sorted(remove)
    pref_remove = [0]
    for x in remove_asc:
        pref_remove.append(pref_remove[-1] + x)

    # Prefix sums of fixed additions in increasing order.
    pref_add = [0]
    for x in add:
        pref_add.append(pref_add[-1] + x)

    # q_remove = sum(weight * number of removal-phase operations
    # for which that weight is still on).
    q_remove = 0
    for pos, x in enumerate(remove, 1):
        q_remove += x * (d - pos + 1)

    # q_add = sum(weight * number of addition-phase operations
    # for which that weight is on).
    q_add = 0
    for pos, x in enumerate(add, 1):
        q_add += x * (u - pos + 1)

    # After required removals, required additions are still off.
    base_middle_sum = final_sum - add_sum

    answer = d * initial_sum - q_remove + u * base_middle_sum + q_add

    # Temporarily disabled common-one coordinates form a decreasing prefix.
    common.sort(reverse=True)

    selected_sum = 0
    s = 0

    for x in common:
        # Insert x into decreasing removal order after fixed weights >= x.
        idx_ge_remove = bisect_left(remove_asc, x)
        cnt_ge_remove = d - idx_ge_remove
        sum_ge_remove = pref_remove[d] - pref_remove[idx_ge_remove]

        # Already selected common weights are all >= x and are before x.
        q_remove += sum_ge_remove + selected_sum + x * (d - cnt_ge_remove + 1)

        # Insert x into increasing addition order after fixed weights <= x.
        idx_le_add = bisect_right(add, x)
        cnt_le_add = idx_le_add
        sum_le_add = pref_add[idx_le_add]

        # Fixed additions <= x occur before x; selected common weights occur after it.
        q_add += sum_le_add + x * (u - cnt_le_add + s + 1)

        selected_sum += x
        s += 1

        removals_count = d + s
        additions_count = u + s

        # Both required additions and selected common coordinates are off here.
        middle_sum = final_sum - add_sum - selected_sum

        cost = (
            removals_count * initial_sum
            - q_remove
            + additions_count * middle_sum
            + q_add
        )
        if cost < answer:
            answer = cost

    print(answer)

if __name__ == "__main__":
    main()