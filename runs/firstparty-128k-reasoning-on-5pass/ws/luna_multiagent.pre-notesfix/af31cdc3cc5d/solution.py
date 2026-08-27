import sys
import heapq


def compute_even_segment_scores(values):
    """Return scores for every even-length prefix of values."""
    low = []   # max-heap of the smallest half, stored as negatives
    high = []  # min-heap of the largest half
    sum_low = 0
    sum_high = 0
    scores = [0] * (len(values) + 1)

    for i, x in enumerate(values, 1):
        if low and x <= -low[0]:
            heapq.heappush(low, -x)
            sum_low += x
        else:
            heapq.heappush(high, x)
            sum_high += x

        desired_low = i // 2

        while len(low) > desired_low:
            y = -heapq.heappop(low)
            sum_low -= y
            heapq.heappush(high, y)
            sum_high += y

        while len(low) < desired_low:
            y = heapq.heappop(high)
            sum_high -= y
            heapq.heappush(low, -y)
            sum_low += y

        if i % 2 == 0:
            scores[i] = sum_high - sum_low

    return scores


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    if n % 2 == 0:
        scores = compute_even_segment_scores(a)
        print(scores[n])
        return

    prefix = compute_even_segment_scores(a)
    suffix = compute_even_segment_scores(a[::-1])

    answer = 0

    # The unmatched element must have an odd 1-based position,
    # i.e. an even zero-based index.
    for p in range(0, n, 2):
        left_length = p
        right_length = n - p - 1
        answer = max(answer, prefix[left_length] + suffix[right_length])

    print(answer)


if __name__ == "__main__":
    main()