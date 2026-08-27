import sys
import heapq


def segment_scores(values):
    """Return F for every even-length prefix, where
    F(segment) = sum of largest half - sum of smallest half.
    """
    n = len(values)
    result = [0] * (n + 1)

    # lo: smaller half, as a max-heap via negation
    # hi: larger half, as a min-heap
    lo = []
    hi = []
    sum_lo = 0
    sum_hi = 0

    for length, x in enumerate(values, 1):
        if hi and x > hi[0]:
            heapq.heappush(hi, x)
            sum_hi += x
        else:
            heapq.heappush(lo, -x)
            sum_lo += x

        target_hi = length // 2

        while len(hi) > target_hi:
            y = heapq.heappop(hi)
            sum_hi -= y
            heapq.heappush(lo, -y)
            sum_lo += y

        while len(hi) < target_hi:
            y = -heapq.heappop(lo)
            sum_lo -= y
            heapq.heappush(hi, y)
            sum_hi += y

        if length % 2 == 0:
            result[length] = sum_hi - sum_lo

    return result


def solve():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))

    if n % 2 == 0:
        a.sort(reverse=True)
        half = n // 2
        answer = 2 * sum(a[:half]) - sum(a)
        print(answer)
        return

    # Prefix scores for even-length prefixes.
    prefix = segment_scores(a)

    # Suffix scores for even-length suffixes.
    suffix_reversed = segment_scores(a[::-1])
    suffix = [0] * (n + 1)
    for length in range(0, n + 1):
        if length % 2 == 0:
            suffix[n - length] = suffix_reversed[length]

    # The unmatched position must have odd 1-based index.
    answer = 0
    for u in range(1, n + 1, 2):
        answer = max(answer, prefix[u - 1] + suffix[u])

    print(answer)


if __name__ == "__main__":
    solve()