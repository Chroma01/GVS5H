import sys
import heapq


def half_difference(values):
    n = len(values)
    result = [0] * (n + 2)

    lower = []  # max-heap via negation: smaller half
    upper = []  # min-heap: larger half
    sum_lower = 0
    sum_upper = 0

    for i, x in enumerate(values, 1):
        if not lower or x <= -lower[0]:
            heapq.heappush(lower, -x)
            sum_lower += x
        else:
            heapq.heappush(upper, x)
            sum_upper += x

        while len(lower) > len(upper) + 1:
            v = -heapq.heappop(lower)
            sum_lower -= v
            heapq.heappush(upper, v)
            sum_upper += v

        while len(upper) > len(lower):
            v = heapq.heappop(upper)
            sum_upper -= v
            heapq.heappush(lower, -v)
            sum_lower += v

        if i % 2 == 0:
            result[i] = sum_upper - sum_lower

    return result


def main():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    prefix = half_difference(a)

    reversed_suffix = half_difference(a[::-1])
    suffix = [0] * (n + 2)
    for start in range(1, n + 1):
        length = n - start + 1
        suffix[start] = reversed_suffix[length]

    if n % 2 == 0:
        print(prefix[n])
        return

    answer = 0
    for survivor in range(1, n + 1, 2):
        answer = max(answer, prefix[survivor - 1] + suffix[survivor + 1])

    print(answer)


if __name__ == "__main__":
    main()