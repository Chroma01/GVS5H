import sys


def avoid_count(positions, n):
    """Number of subarrays containing none of the given sorted positions."""
    prev = 0
    result = 0
    for p in positions:
        gap = p - prev - 1
        result += gap * (gap + 1) // 2
        prev = p
    gap = n - prev
    return result + gap * (gap + 1) // 2


def avoid_count_union(a, b, n):
    """Number of subarrays avoiding all positions in the merge of sorted lists a and b."""
    i = j = 0
    la, lb = len(a), len(b)
    prev = 0
    result = 0

    while i < la or j < lb:
        if j == lb or (i < la and a[i] < b[j]):
            p = a[i]
            i += 1
        else:
            p = b[j]
            j += 1

        gap = p - prev - 1
        result += gap * (gap + 1) // 2
        prev = p

    gap = n - prev
    return result + gap * (gap + 1) // 2


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    pos = [[] for _ in range(n + 1)]

    for i in range(1, n + 1):
        pos[data[i]].append(i)

    total = n * (n + 1) // 2

    avoid = [0] * (n + 1)
    distinct_sum = 0

    for v in range(1, n + 1):
        avoid[v] = avoid_count(pos[v], n)
        distinct_sum += total - avoid[v]

    adjacent_pair_sum = 0

    for x in range(1, n):
        avoid_both = avoid_count_union(pos[x], pos[x + 1], n)
        contains_both = total - avoid[x] - avoid[x + 1] + avoid_both
        adjacent_pair_sum += contains_both

    print(distinct_sum - adjacent_pair_sum)


if __name__ == "__main__":
    main()