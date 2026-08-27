import sys
import heapq


def half_difference_prefix(a):
    """res[i] = largest half sum - smallest half sum for a[:i], when i is even."""
    n = len(a)
    res = [0] * (n + 1)

    lower = []  # max-heap via negatives: smaller half (and one extra when odd)
    upper = []  # min-heap: largest floor(length / 2) elements
    sum_lower = 0
    sum_upper = 0

    for i, x in enumerate(a, 1):
        if upper and x >= upper[0]:
            heapq.heappush(upper, x)
            sum_upper += x
        else:
            heapq.heappush(lower, -x)
            sum_lower += x

        target_upper_size = i // 2

        while len(upper) > target_upper_size:
            y = heapq.heappop(upper)
            sum_upper -= y
            heapq.heappush(lower, -y)
            sum_lower += y

        while len(upper) < target_upper_size:
            y = -heapq.heappop(lower)
            sum_lower -= y
            heapq.heappush(upper, y)
            sum_upper += y

        if i % 2 == 0:
            res[i] = sum_upper - sum_lower

    return res


def main():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    prefix = half_difference_prefix(a)

    if n % 2 == 0:
        print(prefix[n])
        return

    # suffix[i] is the value for A[i-1 : N], indexed with 1-based start i.
    reversed_values = half_difference_prefix(a[::-1])
    suffix = [0] * (n + 2)
    for start in range(1, n + 1):
        length = n - start + 1
        if length % 2 == 0:
            suffix[start] = reversed_values[length]

    answer = 0
    # The unpaired position must be odd in 1-based indexing.
    for unpaired in range(1, n + 1, 2):
        answer = max(answer, prefix[unpaired - 1] + suffix[unpaired + 1])

    print(answer)


if __name__ == "__main__":
    main()