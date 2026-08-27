import sys
from heapq import heappush, heappop


def prefix_even_scores(arr):
    lower = []  # max-heap of the smallest floor(t/2) values, stored negated
    upper = []  # min-heap of the largest ceil(t/2) values
    sum_lower = 0
    sum_upper = 0
    len_lower = 0
    len_upper = 0

    scores = [0]  # scores[k] = best score for prefix length 2*k
    append = scores.append

    for i, x in enumerate(arr, 1):
        if len_lower and x <= -lower[0]:
            heappush(lower, -x)
            sum_lower += x
            len_lower += 1
        else:
            heappush(upper, x)
            sum_upper += x
            len_upper += 1

        target_lower = i >> 1
        if len_lower > target_lower:
            v = -heappop(lower)
            sum_lower -= v
            len_lower -= 1
            heappush(upper, v)
            sum_upper += v
            len_upper += 1
        elif len_upper > i - target_lower:
            v = heappop(upper)
            sum_upper -= v
            len_upper -= 1
            heappush(lower, -v)
            sum_lower += v
            len_lower += 1

        if (i & 1) == 0:
            append(sum_upper - sum_lower)

    return scores


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    pa = prefix_even_scores(a)

    if n % 2 == 0:
        print(pa[-1])
        return

    pb = prefix_even_scores(reversed(a))
    m = n >> 1
    ans = 0

    for k in range(m + 1):
        v = pa[k] + pb[m - k]
        if v > ans:
            ans = v

    print(ans)


if __name__ == "__main__":
    main()