import sys
import heapq


def half_difference_prefix(a):
    n = len(a)
    result = [0] * (n + 1)

    low = []   # max-heap, stored negated: smaller half
    high = []  # min-heap: larger half
    sum_low = 0
    sum_high = 0

    for i, x in enumerate(a, 1):
        if high and x >= high[0]:
            heapq.heappush(high, x)
            sum_high += x
        else:
            heapq.heappush(low, -x)
            sum_low += x

        while len(high) > len(low) + 1:
            y = heapq.heappop(high)
            sum_high -= y
            heapq.heappush(low, -y)
            sum_low += y

        while len(low) > len(high):
            y = -heapq.heappop(low)
            sum_low -= y
            heapq.heappush(high, y)
            sum_high += y

        if i % 2 == 0:
            result[i] = sum_high - sum_low

    return result


def main():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    prefix = half_difference_prefix(a)

    if n % 2 == 0:
        print(prefix[n])
        return

    reversed_prefix = half_difference_prefix(a[::-1])
    suffix = [0] * (n + 1)
    for i in range(n + 1):
        suffix[i] = reversed_prefix[n - i]

    answer = 0
    # Leftover original index is odd in 1-based indexing, hence even in 0-based.
    for k in range(0, n, 2):
        answer = max(answer, prefix[k] + suffix[k + 1])

    print(answer)


if __name__ == "__main__":
    main()