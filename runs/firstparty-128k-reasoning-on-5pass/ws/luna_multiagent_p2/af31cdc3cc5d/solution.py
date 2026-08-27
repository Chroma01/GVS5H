import sys
import heapq


def even_prefix_scores(values):
    """Return F(values[:i]) for every even i, where
    F(S) = sum of largest |S|/2 elements - sum of smallest |S|/2 elements.
    """
    n = len(values)
    result = [0] * (n + 1)

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

        target_lower = (i + 1) // 2
        while len(lower) > target_lower:
            x_move = -heapq.heappop(lower)
            sum_lower -= x_move
            heapq.heappush(upper, x_move)
            sum_upper += x_move

        while len(lower) < target_lower:
            x_move = heapq.heappop(upper)
            sum_upper -= x_move
            heapq.heappush(lower, -x_move)
            sum_lower += x_move

        if i % 2 == 0:
            result[i] = sum_upper - sum_lower

    return result


def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    if n % 2 == 0:
        b = sorted(a)
        half = n // 2
        answer = sum(b[half:]) - sum(b[:half])
        print(answer)
        return

    prefix = even_prefix_scores(a)
    reversed_prefix = even_prefix_scores(a[::-1])

    suffix = [0] * (n + 1)
    for start in range(n + 1):
        length = n - start
        if length % 2 == 0:
            suffix[start] = reversed_prefix[length]

    answer = 0
    for unmatched in range(0, n, 2):
        answer = max(answer, prefix[unmatched] + suffix[unmatched + 1])

    print(answer)


if __name__ == "__main__":
    solve()